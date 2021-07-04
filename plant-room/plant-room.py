#!/usr/bin/env python3
import csv
from datetime import datetime as datetime
import os
import serial

OUTPUT_FILE = os.getcwd() + '/results.csv'


def convert_to_percent(value: int) -> int:
    WATER = 250  # 100%
    AIR = 500  # 0%
    percent = 100 / WATER * (AIR - value)
    return round(percent, 2)


def write_to_csv(raw_value: int, percent_value: int) -> None:
    add_headers = False
    if os.path.isfile(OUTPUT_FILE) is False:
        add_headers = True

    with open(OUTPUT_FILE, 'a') as csvfile:
        timestamp = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
        fieldnames = ['timestamp', 'raw_value', 'percent_value']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if add_headers:
            writer.writeheader()
        writer.writerow({'timestamp': timestamp,
                         'raw_value': raw_value,
                         'percent_value': percent_value})


if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.flush()

    measurement = []
    # Get mean measurement of 3 readings.
    while len(measurement) < 3:
        if ser.in_waiting > 0:
            value = ser.readline().decode('utf-8').strip()
            if len(value) == 3:  # Sometimes first value is corrupted
                measurement.append(int(value))
    value = int(sum(measurement) / len(measurement))
    percent = convert_to_percent(value)
    write_to_csv(value, percent)
    print(f'Plant hydrated in {percent}%. ({value})')
