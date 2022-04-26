#!/usr/bin/env python3
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.orm import declarative_base, Session

load_dotenv()

Base = declarative_base()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


class Measurement(Base):
    __tablename__ = "measurment"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    raw_value = Column(Integer)
    percent_value = Column(Float)

    def __repr__(self):
        return f"Measurment {self.id!r} made at {self.timestamp!r}: {self.raw_value!r} ({self.percent_value!r})."


def add_to_db(raw_value: int, percent_value: float) -> None:
    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        logging.info("DB configuration not specified; omitting this step.")
    else:
        url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            timestamp = datetime.now()
            measurement = Measurement(
                timestamp=timestamp, raw_value=raw_value, percent_value=percent_value)
            session.add(measurement)
            session.commit()
