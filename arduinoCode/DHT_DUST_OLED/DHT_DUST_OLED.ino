//按鈕
const int buttonPin = 5;
int buttonState = 0;
int buttonState_old = 0;
bool stateChange = false;

// OLED
#include <Wire.h>  //載入I2C函式庫
#include <SeeedOLED.h> //載入SeeedOLED函式庫
char info[] = "None";
int oldSize = 4, newSize = 0;

// DHT
#include "DHT.h"
#define DHTPIN A0
#define DHTTYPE DHT11 
DHT dht(DHTPIN, DHTTYPE);

// Dust Sensor
int dustPin = 8; 
unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 2000;
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float concentration = 0;
float concentrationPM25_ugm3;

// Send using wifi
#include <Bridge.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
  dht.begin();

  // Dust Sensor
  pinMode(dustPin, INPUT);
  starttime = millis();//get the current time;
  
  // Button
  pinMode(buttonPin, INPUT);
  
  // OLED
  Wire.begin();
  SeeedOled.init();  
  SeeedOled.clearDisplay();  //清除螢幕
  SeeedOled.setNormalDisplay(); //設定螢幕為正常模式(非反白)
  SeeedOled.setPageMode();  //設定尋址模式頁模式
  SeeedOled.setTextXY(0,0); //設定啟始坐標
  SeeedOled.putString("Smart Satchel"); 
  //SeeedOled.setTextXY(5,0);
  //SeeedOled.putString("No message");

  //Bridge
  Bridge.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
  buttonState = digitalRead(buttonPin);
  Serial.println(buttonState);
  if (buttonState != buttonState_old){
    SeeedOled.clearDisplay();
  }
  buttonState_old = buttonState;
//  if (stateChange == ture){
//     SeeedOled.clearDisplay();
//     stateChange = false;
//  }
  
  float h = dht.readHumidity();
  float t = dht.readTemperature();
      
  Serial.print("DHT-Humidity: "); 
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("DHT-Temperature: "); 
  Serial.print(t);
  Serial.print(" *C\t");

  // Dust Sensor
  duration = pulseIn(dustPin, LOW);
  lowpulseoccupancy = lowpulseoccupancy+duration;
  ratio = lowpulseoccupancy/(sampletime_ms*10.0);  // Integer percentage 0=&gt;100
  concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve
  
  Serial.print("concentration = ");
  Serial.print(concentration);
  Serial.print(" pcs/0.01cf");
  
  concentrationPM25_ugm3 = conversion25(concentration);
  Serial.print("PM25: ");
  Serial.print(concentrationPM25_ugm3);
  Serial.println(" ug/m3");
        
  lowpulseoccupancy = 0;
  starttime = millis();
  
  // Read the State of the pushbutton value

  // OLED
  if (buttonState == 0){
    SeeedOled.setTextXY(0,0); //設定啟始坐標
    SeeedOled.putString("Smart Satchel");
    SeeedOled.setTextXY(1,0); //設定啟始坐標
    SeeedOled.putString("Temp: "); 
    SeeedOled.putNumber(t); 
    SeeedOled.putString(" *C"); 
    SeeedOled.setTextXY(2,0); //設定啟始坐標
    SeeedOled.putString("Humidity: "); 
    SeeedOled.putNumber(h); 
    SeeedOled.putString(" %"); 
    SeeedOled.setTextXY(3,0); //設定啟始坐標
    SeeedOled.putString("Dust: "); 
    SeeedOled.putFloat(concentration,2);
    SeeedOled.setTextXY(4,0); //設定啟始坐標
    SeeedOled.putString("PM25: "); 
    SeeedOled.putFloat(concentrationPM25_ugm3,2);
    SeeedOled.setTextXY(5,0); //設定啟始坐標
    SeeedOled.putString(info); 
  }

  if (buttonState == 1){
    SeeedOled.setTextXY(0,0);
    SeeedOled.putString("Date: ");
    SeeedOled.putString("Monday");
    SeeedOled.setTextXY(1,0);
    SeeedOled.putString("English Chinese");
    SeeedOled.setTextXY(2,0);
    SeeedOled.putString("Math Music");
    
}
   
  //Bridge
  Bridge.put("t",String(t));
  Bridge.put("h",String(h));
  Bridge.put("d",String(concentrationPM25_ugm3));
  Bridge.get("i",info, 6);

  for (int i = 0; i < sizeof(info); i++){
    if (info[i] != '\0')
      newSize ++;
  }
  if (newSize != oldSize){
    SeeedOled.setTextXY(5,0); //設定啟始坐標
    SeeedOled.putString("                ");
    oldSize = newSize;
  }
  newSize = 0;
  
  delay(1000); //每秒回傳一次資料
}

// convert from particles/0.01 ft3 to μg/m3
float conversion25(long concentrationPM25) {
  double pi = 3.14159;
  double density = 1.65 * pow (10, 12);
  double r25 = 0.44 * pow (10, -6);
  double vol25 = (4/3) * pi * pow (r25, 3);
  double mass25 = density * vol25;
  double K = 3531.5;
  return (concentrationPM25) * K * mass25;
}
