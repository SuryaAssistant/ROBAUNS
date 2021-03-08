//PWM = 3, 5, 6, 9, 10, 11 ; 5&6
//Non-PWM = 0, 1, 2, 4, 7, 8, 12, 13

//R_EN and L_EN using the same pin

//pin D7 use for receiving signal from us_modul to
//stopping motor automatically
#define auto_stop 7

//Motor Depan
#define dpn_RPWM 3 
#define dpn_EN 4 
#define dpn_LPWM 5 

//Motor Belakang
#define blkg_RPWM 6 
#define blkg_EN 8 
#define blkg_LPWM 9

//Input Raspi
#define in_dpn_R 2
#define in_dpn_L 11

#define in_blkg_R 12
#define in_blkg_L 13

//Servo
#include<Servo.h>
#define servo_pin 9
Servo kamera_servo;

int i;

// hall sensor
const int hall_sensor =  A0;

//kamera
const int kamera_kanan = A1; //GPIO13
const int kamera_kiri = A2; //GPIO6

int kamera_posisi = 90;

//battery
const int battery_input_pin = A3;
int battery_input_value = 0;


void setup() {
  Serial.begin(9600);

  pinMode(hall_sensor, INPUT);

  pinMode(kamera_kanan, INPUT);
  pinMode(kamera_kiri, INPUT);

  pinMode(battery_input_pin, INPUT);

  //Setting Mode Pin
  pinMode(A2, OUTPUT);
  pinMode(A4, OUTPUT);
  pinMode(A5, OUTPUT);

  
  pinMode(dpn_RPWM, OUTPUT);
  pinMode(dpn_EN, OUTPUT);
  pinMode(dpn_LPWM, OUTPUT);

  pinMode(blkg_RPWM, OUTPUT);
  pinMode(blkg_EN, OUTPUT);
  pinMode(blkg_LPWM, OUTPUT);

  pinMode(in_dpn_R, INPUT);
  pinMode(in_dpn_L, INPUT);

  pinMode(in_blkg_R, INPUT);
  pinMode(in_blkg_L, INPUT);

  //Kamera_servo
  kamera_servo.attach(servo_pin);

  //Set servo 0 degree
  kamera_servo.write(kamera_posisi);

  //Setting awal pin LOW
  digitalWrite(dpn_EN, LOW);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM,0);
  
  digitalWrite(blkg_EN, LOW);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, 0);

  digitalWrite(A4, LOW);
  digitalWrite(A5, LOW);
  digitalWrite(A2, HIGH);

  delay(1000);

  
}

void loop() {
  int status_kanan = digitalRead(in_dpn_R);
  int status_kiri = digitalRead(in_dpn_L);
  int status_maju = digitalRead(in_blkg_R);
  int status_mundur = digitalRead(in_blkg_L);
  int status_auto_stop = digitalRead(auto_stop);
  ///int status_tengah = digitalRead

  int read_kamera_kanan = digitalRead(kamera_kanan);
  int read_kamera_kiri = digitalRead(kamera_kiri);  

/*
  //hall_sensor
  int hall_value = analogRead(hall_sensor);
  if(status_kanan == HIGH){
    //jika roda berada di tengah, gerak saja
    if (hall_value < 500){
      kanan();
    }
    //jika roda tidak di tengah, gerak saja. 
    //tunggu beberapa saat 
    //Jika roda sampai tengah, diam.
    if(hall_value > 500){
      kanan();
      delay(100);
      if (hall_value < 500){
        dpn_diam();
      }
    }
  }
  if(status_kiri == HIGH){
    //jika roda berada di tengah, gerak saja
    if (hall_value < 500){
      kiri();
    }
    //jika roda tidak di tengah, gerak saja. tunggu beberapa saat 
    //Jika roda sampai tengah, diam.
    if(hall_value > 500){
      kiri();
      delay(100);
      if (hall_value < 500){
        dpn_diam();
      }
    }
  }
*/
//-----------------------Kamera------------------
  if(read_kamera_kanan == HIGH){
      kamera_servo.write(kamera_posisi+45);
      read_kamera_kanan == LOW;
  }
  
  if(read_kamera_kiri == HIGH){
      kamera_servo.write(kamera_posisi-45);
      read_kamera_kiri == LOW;
  } 

//-----------------------Baterai------------------
  battery_input_value = analogRead(battery_input_pin);
  //Konversi ADC ke nilai tegangan

//-------------------------Motor------------------
  if(status_kanan == HIGH){
    kanan();
  }
  if(status_kiri == HIGH){
    kiri();
  }  
  if(status_kanan == LOW && status_kiri == LOW){
    dpn_diam();
  }

  if(status_maju == HIGH){
    maju();
  }

  if(status_mundur == HIGH){
    mundur();
  }

  if(status_maju == HIGH && status_mundur == HIGH){
    digitalWrite(A2, HIGH);
    digitalWrite(A4, LOW);
    digitalWrite(A5, LOW);
    //blkg_diam2();
  }

  if(status_auto_stop == HIGH){
    blkg_diam2();
  }

  Serial.print(digitalRead(2));
    Serial.print("         ");
  Serial.print(digitalRead(11));
    Serial.print("         ");
  Serial.print(digitalRead(12));
    Serial.print("         ");
  Serial.println(digitalRead(13));
}

/*
 * Gerakan roda depan -----------------------------------
 */
void kanan(){
  digitalWrite(dpn_EN, HIGH);
  analogWrite(dpn_RPWM, 125);
  analogWrite(dpn_LPWM, 0);
}

void kiri(){
  digitalWrite(dpn_EN, HIGH);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM, 125);
}

/*
 * Gerakan roda belakang --------------------------------
 */
 
void maju(){
  digitalWrite(A2, LOW);
  digitalWrite(A4, LOW);
  digitalWrite(A5, HIGH);
  
  //digitalWrite(blkg_EN, HIGH);
  //analogWrite(blkg_RPWM,90);
  //analogWrite(blkg_LPWM, 225);  
}

void mundur(){
  digitalWrite(A2, LOW);
  digitalWrite(A5, LOW);
  digitalWrite(A4, HIGH);
  
  //digitalWrite(blkg_EN, HIGH);
  //analogWrite(blkg_RPWM, 90);
  //analogWrite(blkg_LPWM, 225);
}

void blkg_diam2(){
  
  //digitalWrite(A2, HIGH);
  //digitalWrite(A4, LOW);
  //digitalWrite(A5, LOW);
  
  //digitalWrite(blkg_EN, LOW);
  //analogWrite(blkg_RPWM, 0);
  //analogWrite(blkg_LPWM, 0);
  
}
/*
 * Stop ----------------------------------------------
 */
 
void dpn_diam(){
  digitalWrite(dpn_EN, LOW);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM, 0);
}

void blkg_diam(){
  
  //digitalWrite(A2, HIGH);
  //digitalWrite(A5, HIGH);
  //digitalWrite(blkg_EN, LOW);
  //analogWrite(blkg_RPWM, 0);
  //analogWrite(blkg_LPWM, 0);
  
}
