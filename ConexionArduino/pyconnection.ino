
char serialData;

void setup() {
  
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600); // aqui se conecta al 9600 con python
}


void loop() {
  if (Serial.available() > 0){
    serialData = Serial.read();
    Serial.print(serialData);
  }
}

          
