#!/usr/bin/env python3
import serial
import time
from prometheus_client import start_http_server, Gauge

# WATER = 250  # 100%
# AIR = 500  # 0%
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
METRIC_PORT = 8000

humidity_value = Gauge('humidity_value', 'Value read from the humidity sensor')

def read_from_serial():
    """Reads a number from the serial port."""
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    if line.isdigit():
                        value = int(line)
                        print(f"Read value: {value}")
                        
                        # Update the Prometheus metric
                        humidity_value.set(value)
                    else:
                        print(f"Received invalid data: {line}")
                except Exception as e:
                    print(f"Error reading serial: {e}")
                time.sleep(55)

if __name__ == "__main__":
    # Start the Prometheus HTTP server
    print(f"Starting Prometheus metrics server on port {METRIC_PORT}")
    start_http_server(METRIC_PORT)
    
    # Read from the serial port and update metrics
    read_from_serial()
