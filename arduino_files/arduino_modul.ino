// Get encoder value from I2C

#include <Wire.h>

//Sensor pins (echo & trigger)
#define trigPin1 4
#define echoPin1 5
#define trigPin2 6
#define echoPin2 7
#define trigPin3 8
#define echoPin3 9

//Pins for direction
#define dir_kanan 10
#define dir_kiri 11


//OUTPUT Ultrasonik tengah 
//Otomatis berhenti
#define auto_stop 13


long duration, distance, Sensor1, Sensor2, Sensor3;

//encoder
int x;
int enc_pos = 0;


int arah_kanan;
int arah_kiri;

// hall sensor
const int hall_sensor=A0;
  
void setup()
{
Wire.begin(9);
Wire.onReceive(receiveEvent);
Serial.begin(9600);   //Serial Port Baudrate: 9600

pinMode(hall_sensor, INPUT);

pinMode(trigPin1, OUTPUT);
pinMode(trigPin2, OUTPUT);
pinMode(trigPin3, OUTPUT);

pinMode(echoPin1, INPUT);
pinMode(echoPin2, INPUT);
pinMode(echoPin3, INPUT);

pinMode(dir_kanan, INPUT);
pinMode(dir_kiri, INPUT);

pinMode(auto_stop, OUTPUT);

digitalWrite(auto_stop, LOW);

}

void receiveEvent(){
  x = Wire.read(); //receive value


  //hall_sensor
  int hall_value = analogRead(hall_sensor);
  if (hall_value < 500 ){
    enc_pos = 0;
  }
  
  //encoder
  if(arah_kanan == HIGH){
     enc_pos = enc_pos + x;
  }

  if(arah_kiri == HIGH){
    enc_pos = enc_pos - x;
  }
  
  //kiri
  SonarSensor(trigPin1, echoPin1);
  Sensor1 = distance;
  
  //tengah
  SonarSensor(trigPin2, echoPin2);
  Sensor2 = distance;
  
  //kanan
  SonarSensor(trigPin3, echoPin3);
  Sensor3 = distance;

  arah_kanan = digitalRead(dir_kanan);
  arah_kiri = digitalRead(dir_kiri);
 

  //Set status

  if(Sensor2 >= 50){
    digitalWrite(auto_stop, LOW);
  }
  
  if(Sensor2 < 50){
    digitalWrite(auto_stop, HIGH);
  }


  //Send to Raspberry Pi
  Serial.print(x);
  Serial.print(",");
  Serial.print(enc_pos);
  Serial.print(",");
  Serial.print(Sensor1);
  Serial.print(",");
  Serial.print(Sensor2);
  Serial.print(",");
  Serial.println(Sensor3);
}

void loop() {
  //
}

void SonarSensor(int trigPin,int echoPin)
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(1);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  delayMicroseconds(10);
}
