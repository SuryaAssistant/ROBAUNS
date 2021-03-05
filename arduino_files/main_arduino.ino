//PWM = 3, 5, 6, 9, 10, 11 ; 5&6
//Non-PWM = 0, 1, 2, 4, 7, 8, 12, 13

//R_EN and L_EN using the same pin


//Motor Depan
#define dpn_RPWM 3 
#define dpn_EN 4 
#define dpn_LPWM 5 

//Motor Belakang
#define blkg_RPWM 6 
#define blkg_EN 8 
#define blkg_LPWM 9


//Servo
#include<Servo.h>
#define servo_pin 9
Servo kamera_servo;

int i;

// kode status perintah raspi
// 10 = motor belakang maju
// 20 = motor belakang mundur
// 30 = motor belakang diam
// 40 = motor depan kanan
// 50 = motor depan kiri
// 60 = motor depan diam
// 70 = kamera ke kanan 30 derajat
// 80 = kamera ke kiri 30 derajat
// 90 = kamera ke tengah
// 100 = kamera diam

int kode_motor_belakang = 30;
int kode_motor_depan = 60;

int kode_kamera = 90;

int kamera_posisi = 90; //derajat
int ubah_posisi_kamera = 30; //derajat

//battery
const int battery_input_pin = A3;
// value from voltage divider
int battery_input_value;
// percentage 
int battery_percent;


void setup() {
  Serial.begin(9600);

  pinMode(battery_input_pin, INPUT);
  
  pinMode(dpn_RPWM, OUTPUT);
  pinMode(dpn_EN, OUTPUT);
  pinMode(dpn_LPWM, OUTPUT);

  pinMode(blkg_RPWM, OUTPUT);
  pinMode(blkg_EN, OUTPUT);
  pinMode(blkg_LPWM, OUTPUT);

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

  delay(1000);
}

void loop() {

  // Read serial from Raspberry Pi
  // data receive in (kode_motor_belakang,kode_motor_depan,kode_kamera)

  if(Serial.available() > 0) {
    kode_motor_belakang = Serial.parseInt();
    kode_motor_depan = Serial.parseInt();
    kode_kamera = Serial.parseInt();
  }

  if(Serial.available() == 0 ){
    kode_motor_belakang = 30;
    kode_motor_depan = 60;
    kode_kamera = 100;
  }


//--------------------Motor Belakang-----------------
  if(kode_motor_belakang == 10){
    maju();
  }

  if(kode_motor_belakang == 20){
    mundur();
  }

  if(kode_motor_belakang == 30){
    blkg_diam();
  }



//-------------------Motor Depan------------------
  if(kode_motor_depan == 40){
    kanan();
  }
  if(kode_motor_depan == 50){
    kiri();
  }  
  if(kode_motor_depan == 60){
    dpn_diam();
  }


//-----------------------Kamera------------------
  if(kode_kamera == 70){
      kamera_servo.write(kamera_posisi + ubah_posisi_kamera);
      //save position
      kamera_posisi = kamera_posisi + ubah_posisi_kamera;
  }
  
  if(kode_kamera == 80){
      kamera_servo.write(kamera_posisi + ubah_posisi_kamera);
      //save position
      kamera_posisi = kamera_posisi + ubah_posisi_kamera;
  } 

  if(kode_kamera == 90){
    kamera_servo.write(90);
  }

  if(kode_kamera == 100){
    kamera_servo.write(kamera_posisi);
  }



//-----------------------Baterai------------------
  battery_input_value = analogRead(battery_input_pin);
  //Konversi ADC ke nilai tegangan
  //Convert battery value to percent
  //max = V (~ADC value); min = V (ADC value);
  battery_percent= map(input_battery, 824, 688, 100, 0);
  //set battery to max 100%
  
  if(battery_percent > 100){
    battery_percent = 100;
  }



  //Send data to Raspberry Pi
  Serial.println(battery_percent);
  
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
  digitalWrite(A4, LOW);
  digitalWrite(A5, HIGH);
  digitalWrite(blkg_EN, HIGH);
  analogWrite(blkg_RPWM,90);
  analogWrite(blkg_LPWM, 225);  
}

void mundur(){
  digitalWrite(A5, LOW);
  digitalWrite(A4, HIGH);
  digitalWrite(blkg_EN, HIGH);
  analogWrite(blkg_RPWM, 90);
  analogWrite(blkg_LPWM, 225);
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
  digitalWrite(blkg_EN, LOW);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, 0);
}