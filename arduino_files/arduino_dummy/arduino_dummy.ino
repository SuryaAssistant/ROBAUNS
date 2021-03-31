/*
   Without encoder
   This code only use for reading ultrasonic sensor value
   and send the data to raspi
*/

#define LED 13


String string_kode_enkripsi;

void setup() {
  Serial.begin(9600);   //Serial Port Baudrate: 9600 (jangan diubah)
}


void loop() {

  //--------------------Detect USBx-----------------
  
  // Read serial from Raspberry Pi
  if (Serial.available()) {
    string_kode_enkripsi = Serial.readStringUntil('\n');
  }

  if (string_kode_enkripsi == "check") {
    //Kirim balasan
    Serial.println("depan");
    Serial.flush();
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
  }
}

