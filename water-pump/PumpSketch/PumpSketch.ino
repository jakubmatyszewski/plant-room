const int button_pin = 2;
const int PUMP_pin = 9;

int button_state;

void setup() {
  pinMode(button_pin, INPUT_PULLUP);
  pinMode(PUMP_pin, OUTPUT);
}

void loop() {
  button_state = digitalRead(button_pin);
  if(button_state == HIGH) {
    digitalWrite(PUMP_pin, LOW);
  } else {
    digitalWrite(PUMP_pin, HIGH);
  }
}
