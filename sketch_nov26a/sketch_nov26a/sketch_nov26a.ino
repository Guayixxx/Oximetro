#include <Wire.h>
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS 1000

PulseOximeter pox;

uint32_t tsLastReport = 0;

// Callback para cuando se detecta un latido
void onBeatDetected() {
    Serial.println("Beat!");
}

void setup() {
    Serial.begin(115200);           // Inicializa la comunicación por Serial (USB)
    
    Serial.print("Inicializando el oxímetro...");
    if (!pox.begin()) {
        Serial.println("FALLÓ");
        for (;;);
    } else {
        Serial.println("ÉXITO");
    }
    
    // Callback para detectar latidos
    pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop() {
    pox.update(); // Actualiza los datos del oxímetro

    // Enviar datos cada segundo
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        float heartRate = pox.getHeartRate();
        float spO2 = pox.getSpO2();

        // Mostrar en el Monitor Serial
        Serial.print("Heart rate: ");
        Serial.print(heartRate);
        Serial.print(" bpm / SpO2: ");
        Serial.print(spO2);
        Serial.println(" %");

        tsLastReport = millis();
    }
}
