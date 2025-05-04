#include <Arduino.h>

// Pin definitions
static constexpr int PUMP_PWM_PIN        =  5;
static constexpr int VALVE_PIN           = 18;
static constexpr int PRESSURE_SENSOR_PIN = 34;  // ADC1_CH6

void setup() {
    Serial.begin(115200);
    pinMode(PUMP_PWM_PIN, OUTPUT);
    pinMode(VALVE_PIN, OUTPUT);
    analogReadResolution(12);
    Serial.println("PulmoAug Controller Initialized");
}

void loop() {
    int raw = analogRead(PRESSURE_SENSOR_PIN);
    float voltage = raw * (3.3f / 4095.0f);
    Serial.print("Pressure sensor V: ");
    Serial.println(voltage, 3);

    // Example: 50% PWM on pump
    ledcSetup(0, 20000, 8);  // channel 0 @ 20 kHz, 8-bit
    ledcAttachPin(PUMP_PWM_PIN, 0);
    ledcWrite(0, 128);

    // Toggle valve every second
    digitalWrite(VALVE_PIN, HIGH);
    delay(1000);
    digitalWrite(VALVE_PIN, LOW);
    delay(1000);
}
