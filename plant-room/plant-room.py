#!/usr/bin/env python3
import csv
import os
import logging
import serial
import statistics
from datetime import datetime

from db import add_to_db

OUTPUT_FILE = os.path.dirname(__file__) + '/results.csv'
WATER = 250  # 100%
AIR = 500  # 0%


def convert_to_percent(value: int) -> int:
    percent = 100 / WATER * (AIR - value)
    return round(percent, 2)


def write_to_csv(raw_value: int, percent_value: int) -> None:
    add_headers = False
    if os.path.isfile(OUTPUT_FILE) is False:
        add_headers = True

    timestamp = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
    data = {
        'timestamp': timestamp,
        'raw_value': raw_value,
        'percent_value': percent_value
    }

    with open(OUTPUT_FILE, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        if add_headers:
            writer.writeheader()
        writer.writerow(data)


if __name__ == "__main__":
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
    except OSError:
        logging.critical("Unable to receive serial signal from the probe.")
    else:
        ser.flush()

        # Get median measurement of 5 readings.
        measurement = []
        while len(measurement) < 5:
            if ser.in_waiting > 0:
                try:
                    value = int(ser.readline().decode('utf-8').strip())
                except (UnicodeDecodeError, ValueError):
                    # sensor reading fails, try again
                    pass
                else:
                    # Sensor can read faulty values at times
                    # so ignore all values outside of realistic range
                    if value > WATER and value < AIR:
                        measurement.append(value)
        final_value = statistics.median(measurement)
        percent = convert_to_percent(final_value)

        write_to_csv(final_value, percent)
        add_to_db(final_value, percent)
        logging.info(f'Plant hydrated in {percent}%. ({final_value})')
