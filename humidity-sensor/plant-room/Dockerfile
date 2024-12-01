FROM python:3.12-slim

WORKDIR /app

COPY plant-room.py /app/plant-room.py
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["python3", "plant-room.py"]
