void setup() {
  Serial.begin(9600); // open serial port, set the baud rate as 9600 bps
}

void loop() {
  int val;
  val = analogRead(0); // connect sensor to Analog 0
  Serial.println(val); // print the value to serial port
  Serial.flush();
  delay(60 * 1000); // 1000 = every second
}
