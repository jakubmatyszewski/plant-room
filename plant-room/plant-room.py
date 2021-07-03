#!/usr/bin/env python3
import csv
from datetime import datetime as datetime
import serial


def convert_to_percent(value: int) -> int:
    WATER = 250  # 100%
    AIR = 500  # 0%
    percent = 100 / WATER * (AIR - value)
    return round(percent, 2)


def write_to_csv(raw_value: int, percent_value: int) -> None:
    with open('results.csv', 'w', newline='') as csvfile:
        timestamp = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
        fieldnames = ['timestamp', 'raw_value', 'percent_value']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'timestamp': timestamp,
                         'raw_value': raw_value,
                         'percent_value': percent_value})


if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            value = ser.readline().decode('utf-8').strip()
            if len(value) == 3:  # Sometimes first value is corrupted
                percent = convert_to_percent(int(value))
                write_to_csv(value, percent)
                print(f'Plant hydrated in {percent}%. ({value})')
                break
