
//Motor Belakang
#define RPWM 10 
#define ENR 8
#define ENL 9
#define LPWM 11
 

int s_f = 230 ;
int s_b = 230 ;
int i = 0 ;
int j = 0 ;

//Input Raspi
#define in_Maju 3
#define in_Mundur 4
#define in_Diam 7

/*
 * Gerakan roda belakang --------------------------------
 */



void maju_C()//kecepatan lanjut, Continous Speed
{
  
  digitalWrite(ENR, HIGH);
  digitalWrite(ENL, HIGH);
  analogWrite(RPWM, 0);
  analogWrite(LPWM, s_f);  
  Serial.println("Maju2");
  
}


void mundur_C()
{
  digitalWrite(ENR, HIGH);
  digitalWrite(ENL, HIGH);
  analogWrite(RPWM, s_b);
  analogWrite(LPWM, 0);
  Serial.println("Mundur2");
  
}

/*
 * Stop ----------------------------------------------
 */
 
void diam()
{
  digitalWrite(ENR, LOW);
  digitalWrite(ENL, LOW);
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);
  Serial.println("Diam");
  
}
/*
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
*/

void setup() 
{
  Serial.begin(9600);
/*
  pinMode(hall_sensor, INPUT);

  pinMode(kamera_kanan, INPUT);
  pinMode(kamera_kiri, INPUT);

  pinMode(battery_input_pin, INPUT);
*/
  //Setting Mode Pin
   
  pinMode(RPWM, OUTPUT);
  pinMode(ENR, OUTPUT);
  pinMode(ENL, OUTPUT);
  pinMode(LPWM, OUTPUT);

  pinMode(in_Mundur, INPUT);
  pinMode(in_Maju, INPUT);

  

  //Setting awal pin HIGH
  digitalWrite(ENR, LOW);
  digitalWrite(ENL, LOW);
  analogWrite(RPWM, 0);
  analogWrite(LPWM,0);
  

  delay(1000);
  
}

void loop() 
{
  
  int status_maju = digitalRead(in_Maju);
  int status_mundur = digitalRead(in_Mundur);
  int status_diam = digitalRead(in_Diam);
  
    
  


//-------------------------Motor------------------
  
  if(status_maju == HIGH)
  {
    j=0;
    i++;
    maju_C();
    delay(1);
    if (i < 99)
    {
      s_f= 230;
    }
    if (i>100)
    {
      s_f = 130;
    }
  }

  if(status_mundur == HIGH)
  {
    i=0;
    j++;
    mundur_C();
    delay(1);
    if (j < 99)
    {
      s_b = 230;
    }
    if (j>100)
    {
      s_b = 130;
    }
  }

  if(status_diam == HIGH)
  {
    diam();
    i=0;
    j=0;
   
  }
}
