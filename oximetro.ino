#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <ArduinoJson.h>  // Incluir la biblioteca ArduinoJson

// Configuración de hardware
#define SDA_PIN 22
#define SCL_PIN 23
#define SERIAL_BAUD 115200
#define REQUIRED_STABLE_READINGS 5
#define FINGER_THRESHOLD 50000
#define RED_THRESHOLD 10000
#define SAMPLE_RATE_HZ 50
#define READ_INTERVAL_MS (1000 / SAMPLE_RATE_HZ)
#define DC_FILTER_ALPHA 0.95
#define AC_BUFFER_SIZE 25
#define SPO2_CALIBRATION_OFFSET 15.0

// Estructuras de datos
struct SensorConfiguration {
  uint8_t ledBrightness;
  uint8_t sampleAverage;
  uint8_t ledMode;
  int sampleRate;
  int pulseWidth;
  int adcRange;
};

struct BiometricData {
  float spO2 = 0.0;
  int bpm = 0;
  float temperature = 0.0;
  bool fingerDetected = false;
};

struct NetworkConfiguration {
  const char* ssid;
  const char* password;
  const char* serverUrl;
};

// Objetos globales
MAX30105 particleSensor;
HTTPClient http;
BiometricData currentData;
NetworkConfiguration networkConfig = {
  "Carlo's",
  "00000000",
  "https://18.212.80.15/data"
};

SensorConfiguration sensorConfig = {
  0x1F,  // LED brightness (0-255)
  4,      // Sample average
  2,      // LED mode
  400,    // Sample rate (Hz)
  411,    // Pulse width
  4096    // ADC range
};

// Variables de estado
long lastBeat = 0;
float beatsPerMinute = 0.0;
int beatAvg = 80;
int stableReadings = 0;

// Componentes AC/DC
float dcRed = 0.0;
float dcIR = 0.0;
float acRedBuffer[AC_BUFFER_SIZE] = {0};
float acIRBuffer[AC_BUFFER_SIZE] = {0};
uint8_t bufferIndex = 0;

// Prototipos de funciones
bool initSensor();
bool connectToWiFi();
void checkNetworkConnection();
void processSensorData();
void updateACDCComponents(long red, long ir);
void calculateSpO2();
void processHeartRate(long irValue);
void sendToServer();
void handleSensorError(const char* message);

void setup() {
  Serial.begin(SERIAL_BAUD);
  Wire.begin(SDA_PIN, SCL_PIN);

  if (!initSensor()) {
    handleSensorError("Falló inicialización del sensor");
  }

  if (!connectToWiFi()) {
    handleSensorError("Falló conexión WiFi");
  }
}

bool initSensor() {
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) return false;
  
  particleSensor.setup(
    sensorConfig.ledBrightness,
    sensorConfig.sampleAverage,
    sensorConfig.ledMode,
    sensorConfig.sampleRate,
    sensorConfig.pulseWidth,
    sensorConfig.adcRange
  );
  
  particleSensor.enableDIETEMPRDY();
  return true;
}

bool connectToWiFi() {
  WiFi.disconnect(true);
  WiFi.begin(networkConfig.ssid, networkConfig.password);

  Serial.print("Conectando a WiFi");
  unsigned long startTime = millis();
  
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startTime > 15000) return false;
    delay(250);
    Serial.print(".");
  }
  
  Serial.println("\nConectado! IP: ");
  Serial.println(WiFi.localIP());
  return true;
}

void loop() {
  static unsigned long lastRead = 0;
  
  if (millis() - lastRead >= READ_INTERVAL_MS) {
    lastRead = millis();
    
    checkNetworkConnection();
    processSensorData();
  }
}

void checkNetworkConnection() {
  if (WiFi.status() != WL_CONNECTED) {
    static unsigned long lastAttempt = 0;
    
    if (millis() - lastAttempt > 5000) {
      lastAttempt = millis();
      connectToWiFi();
    }
  }
}

void processSensorData() {
  long ir = particleSensor.getIR();
  long red = particleSensor.getRed();
  
  currentData.fingerDetected = ir > FINGER_THRESHOLD && red > RED_THRESHOLD;

  if (!currentData.fingerDetected) {
    if (currentData.bpm != 0 || currentData.spO2 != 0) {
      Serial.println("❌ Dedo retirado");
      currentData.bpm = 0;
      currentData.spO2 = 0;
    }
    stableReadings = 0;
    return;
  }

  updateACDCComponents(red, ir);
  processHeartRate(ir);
  calculateSpO2();

  if (stableReadings >= REQUIRED_STABLE_READINGS) {
    sendToServer();
    stableReadings = 0;
  }

  printSensorStatus();
}

void updateACDCComponents(long red, long ir) {
  // Filtrado DC
  dcRed = DC_FILTER_ALPHA * dcRed + (1 - DC_FILTER_ALPHA) * red;
  dcIR = DC_FILTER_ALPHA * dcIR + (1 - DC_FILTER_ALPHA) * ir;

  // Componentes AC
  acRedBuffer[bufferIndex] = red - dcRed;
  acIRBuffer[bufferIndex] = ir - dcIR;
  bufferIndex = (bufferIndex + 1) % AC_BUFFER_SIZE;
}

void calculateSpO2() {
  float rmsRed = 0.0;
  float rmsIR = 0.0;
  
  for (int i = 0; i < AC_BUFFER_SIZE; i++) {
    rmsRed += sq(acRedBuffer[i]);
    rmsIR += sq(acIRBuffer[i]);
  }
  
  rmsRed = sqrt(rmsRed / AC_BUFFER_SIZE);
  rmsIR = sqrt(rmsIR / AC_BUFFER_SIZE);
  
  float ratio = (rmsRed / dcRed) / (rmsIR / dcIR);
  currentData.spO2 = constrain(110.0 - (25.0 * ratio) + SPO2_CALIBRATION_OFFSET, 70.0, 100.0);
}

void processHeartRate(long irValue) {
  if (checkForBeat(irValue)) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    
    float instantBPM = 60000.0 / delta;
    
    if (instantBPM > 30 && instantBPM < 200) {
      // Filtro de mediana móvil
      static float bpmBuffer[5] = {0};
      static uint8_t bpmIndex = 0;
      
      bpmBuffer[bpmIndex] = instantBPM;
      bpmIndex = (bpmIndex + 1) % 5;
      
      // Ordenar y tomar la mediana
      float sorted[5];
      memcpy(sorted, bpmBuffer, sizeof(sorted));
      std::sort(sorted, sorted + 5);
      
      currentData.bpm = sorted[2];
      stableReadings++;
    }
  }
}

void sendToServer() {
  StaticJsonDocument<256> doc;

  // Agregar los datos al documento JSON
  doc["red"] = dcRed;
  doc["ir"] = dcIR;
  doc["spo2"] = currentData.spO2;
  doc["bpm"] = currentData.bpm;
  doc["temp"] = particleSensor.readTemperature();
  doc["t"] = millis();

  // Convertir el JSON a una cadena
  String postData;
  serializeJson(doc, postData);

  // Realizar la solicitud HTTP POST
  http.begin(networkConfig.serverUrl);
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(postData);

  if (httpCode == HTTP_CODE_OK) {
    Serial.println("Datos enviados OK");
  } else {
    Serial.printf("Error HTTP %d: %s\n", httpCode, http.errorToString(httpCode).c_str());
  }

  http.end();
}

void printSensorStatus() {
  static unsigned long lastPrint = 0;
  
  if (millis() - lastPrint > 2000) {
    lastPrint = millis();
    
    Serial.printf("SpO2: %.1f%%, BPM: %d, Temp: %.1fC\n",
      currentData.spO2, currentData.bpm, particleSensor.readTemperature());
  }
}

void handleSensorError(const char* message) {
  Serial.println(message);
  Serial.println("Reiniciando en 5 segundos...");
  delay(5000);
  ESP.restart();
}