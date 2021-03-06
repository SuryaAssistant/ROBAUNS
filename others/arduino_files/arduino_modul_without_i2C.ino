// Without encoder
// This code only use for reading ultrasonic sensor value


// Sensor pins (echo & trigger)
#define trigPin1 4
#define echoPin1 5
#define trigPin2 6
#define echoPin2 7
#define trigPin3 8
#define echoPin3 9

long duration, distance, Sensor1, Sensor2, Sensor3;

  
void setup(){
Serial.begin(9600);   //Serial Port Baudrate: 9600 (jangan diubah)

pinMode(trigPin1, OUTPUT);
pinMode(trigPin2, OUTPUT);
pinMode(trigPin3, OUTPUT);

pinMode(echoPin1, INPUT);
pinMode(echoPin2, INPUT);
pinMode(echoPin3, INPUT);
}


void loop() {
  
  //kiri
  SonarSensor(trigPin1, echoPin1);
  Sensor1 = distance;
  
  //tengah
  SonarSensor(trigPin2, echoPin2);
  Sensor2 = distance;
  
  //kanan
  SonarSensor(trigPin3, echoPin3);
  Sensor3 = distance;

  //Send ultrasonic value to Raspberry Pi
  Serial.print(Sensor1);
  Serial.print(",");
  Serial.print(Sensor2);
  Serial.print(",");
  Serial.println(Sensor3);
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
