// ======== Blynk Template Info ========
#define BLYNK_TEMPLATE_ID "TMPL3_pIAuEZW"
#define BLYNK_TEMPLATE_NAME "Smart Agriculture"
#define BLYNK_AUTH_TOKEN "DlSb-mOUyFqzzKa5APyhnpCut4jN1sog"
// ======== Libraries ========
#include <WiFi.h>
#include <BlynkSimpleEsp32.h>
#include <DHT.h>

// ======== WiFi Credentials ========
char ssid[] = "Hiii";         // 👉 Replace with your WiFi name
char pass[] = "9903249226";     // 👉 Replace with your WiFi password

// ======== Sensor Pins ========
#define DHTPIN 4            // DHT22 on GPIO 4
#define DHTTYPE DHT22
#define SOIL_PIN 32         // Soil Moisture Sensor on GPIO 32
#define RAIN_PIN 33         // Rain Sensor on GPIO 33
#define PH_PIN 34           // pH Sensor on GPIO 34

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

  Serial.println("Connecting to WiFi...");
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
  Serial.println("Connected to Blynk!");
}

void loop() {
  Blynk.run();

  // ======= DHT22 =======
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // ======= Soil Moisture =======
  int soilRaw = analogRead(SOIL_PIN);
  float soilMoisture = map(soilRaw, 0, 4095, 100, 0);  // Dry = high value

  // ======= Rainfall (Approx mm) =======
  int rainRaw = analogRead(RAIN_PIN);
  float rainMM = 0.0;
  if (rainRaw >= 3500) rainMM = 0.0;
  else if (rainRaw >= 3000) rainMM = 0.5;
  else if (rainRaw >= 2000) rainMM = 1.5;
  else if (rainRaw >= 1500) rainMM = 2.5;
  else if (rainRaw >= 1000) rainMM = 4.0;
  else rainMM = 6.0;

  // ======= pH Sensor =======
  int phRaw = analogRead(PH_PIN);
  float phVoltage = phRaw * (3.3 / 4095.0);
  float pH = 7 + ((2.5 - phVoltage) / 0.18);  // Calibrate for your sensor

  // ======= Debug to Serial Monitor =======
  Serial.println("===== Sensor Readings =====");
  Serial.printf("Temperature: %.2f °C\n", temperature);
  Serial.printf("Humidity: %.2f %%\n", humidity);
  Serial.printf("Soil Moisture: %.2f %%\n", soilMoisture);
  Serial.printf("Rainfall: %.2f mm\n", rainMM);
  Serial.printf("pH Level: %.2f\n", pH);
  Serial.println("============================");

  // ======= Send to Blynk App =======
  Blynk.virtualWrite(V0, temperature);       // Temperature
  Blynk.virtualWrite(V1, humidity);          // Humidity
  Blynk.virtualWrite(V2, soilMoisture);      // Soil Moisture
  Blynk.virtualWrite(V3, rainMM);            // Rainfall (mm)
  Blynk.virtualWrite(V4, pH);                // pH Level

  if (soilMoisture < 35) {
    Blynk.logEvent("low_soil", "⚠️ Soil moisture is low!");
  }

  if (temperature > 40) {
    Blynk.logEvent("high_temp", "🔥 High Temperature Alert!");
  }

  if (rainMM > 20) {
    Blynk.logEvent("rain_detected", "🌧 Rain Detected!");
  }

  if (pH < 5.5 || pH > 8.0) {
    Blynk.logEvent("pH_alert", "⚠️ Soil pH out of healthy range!");
  }

  delay(2000);  // Wait 2 seconds before next reading
}
