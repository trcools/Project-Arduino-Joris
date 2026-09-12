import serial
import csv
import time

# Pas de poort aan naar die van jouw Arduino (bijv. 'COM3' op Windows of '/dev/cu.usbmodem...' op Mac)
serial_port = '/dev/cu.usbmodem206EF130D6D82' 
baud_rate = 115200
output_file = "magnetometer_data.csv"

ser = serial.Serial(serial_port, baud_rate, timeout=1)
time.sleep(2) # Geef de Arduino tijd om te resetten

print("Start met loggen... Druk op Ctrl+C om te stoppen.")

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Schrijf de header
    writer.writerow(["Timestamp", "B_x", "B_y", "B_z"])
    
    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Verwacht formaat: "B_x_uT:12.30,B_y_uT:45.60,B_z_uT:78.90"
                # We halen hier de pure getallen uit
                try:
                    parts = line.split(',')
                    bx = parts[0].split(':')[1]
                    by = parts[1].split(':')[1]
                    bz = parts[2].split(':')[1]
                    
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([timestamp, bx, by, bz])
                    print(f"{timestamp} -> X: {bx} uT | Y: {by} uT | Z: {bz} uT")
                except IndexError:
                    # Sla incomplete regels (zoals bij het opstarten) over
                    continue
    except KeyboardInterrupt:
        print("\nLoggen gestopt. Data opgeslagen in:", output_file)
    finally:
        ser.close()