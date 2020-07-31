/***************************************************************************
  This is software was created by Giacomo Marchioro 
  from the library for the BME680 gas, humidity, temperature & pressure sensor
  designed specifically to work with the Adafruit BME680 Breakout
  ----> http://www.adafruit.com/products/3660

  These sensors use I2C or SPI to communicate, 2 or 4 pins are required
  to interface.

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing products
  from Adafruit!

  Written by Giacomo Marchioro modifying Limor Fried & Kevin Townsend for Adafruit Industries.
  BSD license, all text above must be included in any redistribution.

 ***************************************************************************/

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME680 bme; // I2C
//Adafruit_BME680 bme(BME_CS); // hardware SPI
//Adafruit_BME680 bme(BME_CS, BME_MOSI, BME_MISO,  BME_SCK);

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println(F("BME680 test"));

  if (!bme.begin()) {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while (1);
  }

  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150); // 320*C for 150 ms

}

// current values
  int cRH;
  int cT;
  long cP;
  long cOhm;
  // previus values
  int prevRH = int(bme.humidity*100);
  int prevT = int(bme.temperature*100);
  long prevP = bme.pressure;
  long prevOhm = long(bme.gas_resistance);
  // comulative differences
  int cdiffRH = 0;
  int cdiffT = 0;
  long cdiffP = 0;
  long cdiffOhm = 0;
  // Thresholds
  int TdiffRH = 100; // 1 percent
  int TdiffT = 100; // 1 degree 
  long TdiffP = 100; // 1 hPascal
  int TdiffOhm = 7000;
  bool changed = false;
  int cycles_count = 0;
  bool debug = false;
  bool starting = true;

void loop() {
  if (! bme.performReading()) {
    Serial.println("Failed to perform reading :(");
    return;
  }
  if (starting){
       prevRH = int(bme.humidity*100);
       prevT = int(bme.temperature*100);
       prevP = bme.pressure;
       prevOhm = bme.gas_resistance;
       starting = false;
  };
  // current measurment
  cRH = bme.humidity*100;
  // cumulative difference
  cdiffRH += (prevRH - cRH);
  // current meas becoms previus
  prevRH = cRH;

  // current measurment
  cP = bme.pressure;
  // cumulative difference
  cdiffP += (prevP - cP);
  // current meas becoms previus
  prevP = cP;

   // current measurment
  cT = bme.temperature*100;
  // cumulative difference
  cdiffT += (prevT - cT);
  // current meas becoms previus
  prevT = cT;

    // current measurment
  cOhm= bme.gas_resistance;
  // cumulative difference
  cdiffOhm += (prevOhm - cOhm);
  // current meas becoms previus
  prevOhm = cOhm;

  if(debug){
      Serial.print("Difference;");
      Serial.print(cdiffT);
      Serial.print(";*cC;");
      Serial.print(cdiffP);
      Serial.print(";Pa;");
      Serial.print(cdiffRH);
      Serial.print(";%*100;");
      Serial.print(cdiffOhm);
      Serial.println(";Ohms");
      Serial.print("Previus;");
      Serial.print(prevT);
      Serial.print(";*cC;");
      Serial.print(prevP);
      Serial.print(";Pa;");
      Serial.print(prevRH);
      Serial.print(";%*100;");
      Serial.print(prevOhm);
      Serial.println(";Ohms");
    };
  // at leas every hour we take a measurment even if nothing happen
  if (cycles_count > 1800){
    changed = true;
    cycles_count = 0;
   };
  if (abs(cdiffRH) > TdiffRH){
    changed = true;
    cdiffRH = 0;
    cycles_count = 0;
   };
  if (abs(cdiffT) > TdiffT){
    changed = true;
    cdiffT = 0;
    cycles_count = 0;
    };
  if (abs(cdiffP) > TdiffP){
    changed = true;
    cdiffP = 0;
    cycles_count = 0;
    };
  if (abs(cdiffOhm) > TdiffOhm){
    changed = true;
    cdiffOhm = 0;
    cycles_count = 0;
    };
    
  if(changed){
    Serial.print("START;");
    Serial.print(cT);
    Serial.print(";*cC;");
    Serial.print(cP);
    Serial.print(";Pa;");
    Serial.print(cRH);
    Serial.print(";%*100;");
    Serial.print(cOhm);
    Serial.println(";Ohms");
    changed = false;
  };
  
  delay(2000);
  cycles_count+=1;
}
