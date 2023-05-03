#!/usr/bin/env python3
import logging
import serial
import statistics

from db import add_to_db, write_to_csv

WATER = 250  # 100%
AIR = 500  # 0%


def convert_to_percent(value: int) -> int:
    percent = 100 / WATER * (AIR - value)
    return round(percent, 2)


if __name__ == "__main__":
    with serial.Serial('/dev/ttyACM0', 9600) as ser:
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
