/*
   Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleScan.cpp
   Ported to Arduino ESP32 by Evandro Copercini
*/

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

int scanTime = 5; //In seconds
BLEScan* pBLEScan;


String Names[10];
int Device_RSSI[10];
// index del arreglo spara nombres y RSSI 
int scan_position=0;

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      //Serial.printf("Advertised Device: %s \n", advertisedDevice.toString().c_str());
        //Serial.print("  RSSI:");
        //Serial.println(advertisedDevice.getRSSI());
        if(advertisedDevice.haveName()== true){
                  Names[scan_position]= advertisedDevice.getName().c_str();
                  Device_RSSI[scan_position]=advertisedDevice.getRSSI();
                  scan_position ++; 
          }

    }
};

void setup() {
  Serial.begin(115200);
  Serial.println("Scanning...");
  

  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);  // less or equal setInterval value

      // Limpiar los dos Array 
  for (int i=0; i< (sizeof(Device_RSSI)/sizeof(Device_RSSI[0]));i++){
    Device_RSSI[i]=0;
  }
   for (int i=0; i< (sizeof(Names)/sizeof(Names[0]));i++){
    Names[i]="";
  }
}

void loop() {
  BLEDevice::init("");
  // put your main code here, to run repeatedly:
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  //Serial.print("Devices found: ");
  //Serial.println(foundDevices.getCount());
  //Serial.println("Scan done!");
  PrintJSON();
  pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory
  
  scan_position=0;

  // Limpiar los dos Array 
  for (int i=0; i< (sizeof(Device_RSSI)/sizeof(Device_RSSI[0]));i++){
     Device_RSSI[i]=0;
  }
  for (int i=0; i< (sizeof(Names)/sizeof(Names[0]));i++){
      Names[i]="";
  }
    
  delay(700);
  BLEDevice::deinit(false);
}

void PrintJSON(){
  Serial.print("{\"devices\":[");
  for (int i=0; i< (sizeof(Names)/sizeof(Names[0]));i++){
    if(Names[i]==""){
      Serial.println("]}");
      break;
    }
    else{
      Serial.print("{\"name\":");
      Serial.print("\"");
      Serial.print(Names[i]);
      Serial.print("\",");
      Serial.print("\"rssi\":");
      Serial.print(Device_RSSI[i]);
    
      if(Names[i+1]==""){
        Serial.print("}");
      }
      else{
        Serial.print("},");
      }
    }
  }
  
}
