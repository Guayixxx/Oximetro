import serial
import pandas as pd
from datetime import datetime

# Configuración del puerto serial (USB)
PORT = "/dev/ttyUSB0"  # Cambia esto por tu puerto correcto
BAUD_RATE = 115200
CSV_FILE = "data.csv"

# Inicializar el archivo CSV limpio
def initialize_csv():
    df = pd.DataFrame(columns=["Timestamp", "HeartRate", "SpO2"])
    df.to_csv(CSV_FILE, index=False)
    print(f"Archivo CSV inicializado: {CSV_FILE}")

# Crear conexión serial
try:
    ser = serial.Serial(PORT, BAUD_RATE)
    print(f"Conectado al puerto {PORT} a {BAUD_RATE} baudios.")
except Exception as e:
    print(f"Error al conectar al puerto serial: {e}")
    ser = None

# Leer datos desde Serial
def read_from_serial():
    if ser is None:
        print("El puerto serial no está disponible.")
        return

    while True:
        try:
            # Leer línea desde Serial
            line = ser.readline().decode('utf-8').strip()
            
            # Filtrar datos inválidos
            if "Heart rate: 0.00 bpm" in line and "SpO2: 0.00 %" in line:
                continue  # Ignorar datos inválidos

            # Procesar datos válidos
            if "Heart rate" in line and "SpO2" in line:
                hr_start = line.find("Heart rate:") + len("Heart rate:")
                spo2_start = line.find("SpO2:") + len("SpO2:")
                hr_end = line.find("bpm")
                spo2_end = line.find("%")
                
                # Extraer valores
                heart_rate = float(line[hr_start:hr_end].strip())
                spO2 = float(line[spo2_start:spo2_end].strip())
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Agregar datos al archivo CSV
                with open(CSV_FILE, mode="a") as file:
                    file.write(f"{timestamp},{heart_rate},{spO2}\n")
                print(f"Datos guardados: {timestamp}, HR: {heart_rate}, SpO₂: {spO2}")
        except Exception as e:
            print(f"Error al leer del puerto serial: {e}")

# Iniciar la lectura
if __name__ == "__main__":
    try:
        initialize_csv()  # Limpia el archivo CSV al iniciar
        read_from_serial()
    except KeyboardInterrupt:
        print("Finalizando el recolector de datos.")
        if ser is not None:
            ser.close()
