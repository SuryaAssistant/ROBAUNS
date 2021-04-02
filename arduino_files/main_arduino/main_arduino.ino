/*
   This program used to control the motors of robot
   Upload this program to arduino on top of raspberry pi
*/

//PWM = 3, 5, 6, 9, 10, 11 ; 5&6
//Non-PWM = 0, 1, 2, 4, 7, 8, 12, 13

//R_EN and L_EN using the same pin

#define LED 13

//Motor Depan
#define dpn_RPWM 3
#define dpn_EN 4
#define dpn_LPWM 5

//Motor Belakang
#define blkg_RPWM 6
#define blkg_EN 9
#define blkg_LPWM 11

//Servo
#include<Servo.h>
#define servo_pin 10
Servo kamera_servo;

int i;

// kode status perintah raspi
// 1 = motor belakang maju
// 2 = motor belakang mundur
// 3 = motor belakang diam
// 4 = motor depan kanan
// 5 = motor depan kiri
// 6 = motor depan diam
// 10 = kamera ke kanan 30 derajat
// 11 = kamera ke kiri 30 derajat
// 12 = kamera ke tengah
// 13 = kamera diam


int kode_motor_belakang = 3;
int kode_motor_depan = 6;
int kode_kamera = 13;

int kamera_posisi = 90; //derajat
int ubah_posisi_kamera = 30; //derajat

//battery
const int battery_input_pin = A3;
// value from voltage divider
int battery_input_value;
// percentage
int battery_percent;

String string_kode_enkripsi;
int int_kode_enkripsi;

int motor_pwm = 125;
int prev_motor_belakang = 3;

void setup() {
  Serial.begin(9600);

  pinMode(battery_input_pin, INPUT);

  pinMode(dpn_RPWM, OUTPUT);
  pinMode(dpn_EN, OUTPUT);
  pinMode(dpn_LPWM, OUTPUT);

  pinMode(blkg_RPWM, OUTPUT);
  pinMode(blkg_EN, OUTPUT);
  pinMode(blkg_LPWM, OUTPUT);

  pinMode(LED, OUTPUT);

  //Kamera_servo
  kamera_servo.attach(servo_pin);
  //Set servo 90 degree
  kamera_servo.write(kamera_posisi);
  delay(15);

  //Setting awal pin LOW
  digitalWrite(dpn_EN, LOW);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM, 0);

  digitalWrite(blkg_EN, LOW);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, 0);
}

void loop() {

  // Read serial from Raspberry Pi
  if (Serial.available()) {
    string_kode_enkripsi = Serial.readStringUntil('\n');
  }

  //--------------------Ping dan Dekripsi-----------------

  if (string_kode_enkripsi == "check") {
    //Kirim balasan
    Serial.println("main");
    Serial.flush();
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
  }

  if (string_kode_enkripsi != "check") {

    // ubah ke integer
    int_kode_enkripsi = string_kode_enkripsi.toInt();
    // contoh 11413
    // dekripsi
    kode_motor_belakang = (int_kode_enkripsi - 10000) / 1000;
    kode_motor_depan = ((int_kode_enkripsi - 10000) - (kode_motor_belakang * 1000)) / 100;
    kode_kamera = ((int_kode_enkripsi - 10000) - ((kode_motor_belakang * 1000) + (kode_motor_depan * 100)));
  }
  //    Serial.print(kode_motor_belakang);
  //    Serial.print("-");
  //    Serial.print(kode_motor_depan);
  //    Serial.print("-");
  //    Serial.println(kode_kamera);


  //--------------------Motor Belakang-----------------
  if (kode_motor_belakang == 1) {
    // If previous kode_motor_belakang == 1 and kode_motor_belakang now == 1,
    // increase the motor's pwm signal.
    // else, reset the pwm motor
    if (prev_motor_belakang == 1)
    {
      motor_pwm = motor_pwm + 5;
      // limit the pwm
      if (motor_pwm >= 200)
      {
        motor_pwm = 200;
      }
    }

    else
    {
      motor_pwm = 125;
    }

    maju();
  }

  if (kode_motor_belakang == 2) {
    motor_pwm = 125;
    mundur();
  }

  if (kode_motor_belakang == 3) {
    blkg_diam();
  }



  prev_motor_belakang = kode_motor_belakang;

  //-------------------Motor Depan------------------
  if (kode_motor_depan == 4) {
    kanan();
  }
  if (kode_motor_depan == 5) {
    kiri();
  }
  if (kode_motor_depan == 6) {
    dpn_diam();
  }

  //-----------------------Kamera------------------
  if (kode_kamera == 10) {

    kamera_posisi = kamera_posisi + ubah_posisi_kamera;
    kamera_servo.write(kamera_posisi);
    delay(15);
  }

  if (kode_kamera == 11) {
    kamera_posisi = kamera_posisi - ubah_posisi_kamera;
    kamera_servo.write(kamera_posisi);
    delay(15);
  }

  if (kode_kamera == 12) {
    kamera_posisi = 90;
    kamera_servo.write(kamera_posisi);
    delay(15);
  }

  if (kode_kamera == 13) {
    kamera_servo.write(kamera_posisi);
    delay(15);
  }

  //-----------------------Baterai------------------
  battery_input_value = analogRead(battery_input_pin);
  //Konversi ADC ke nilai tegangan
  //Convert battery value to percent
  //max = 13,2V 3,3V()(~ADC value = 675); min = 12,6V 3,15V(~ADC value = 645);
  battery_percent = map(battery_input_value, 675, 645, 100, 0);
  //set battery to max 100%

  if (battery_percent > 100) {
    battery_percent = 100;
  }

  //Send data to Raspberry Pi
  //Serial.println(battery_percent);

}

/*
   Gerakan roda depan -----------------------------------
*/
void kanan() {
  digitalWrite(dpn_EN, HIGH);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM, 125);
  delay(50);
}

void kiri() {
  digitalWrite(dpn_EN, HIGH);
  analogWrite(dpn_RPWM, 125);
  analogWrite(dpn_LPWM, 0);
  delay(50);
}

/*
   Gerakan roda belakang --------------------------------
*/

void maju() {
  digitalWrite(blkg_EN, HIGH);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, motor_pwm);
  delay(50);
}

void mundur() {
  digitalWrite(blkg_EN, HIGH);
  analogWrite(blkg_RPWM, motor_pwm);
  analogWrite(blkg_LPWM, 0);
  delay(50);
}

/*
   Stop ----------------------------------------------
*/

void dpn_diam() {
  digitalWrite(dpn_EN, LOW);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM, 0);
}

void blkg_diam() {
  digitalWrite(blkg_EN, LOW);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, 0);
}
