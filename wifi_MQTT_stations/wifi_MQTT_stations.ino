// LED will blink when in config mode

#include <WiFiManager.h> // https://github.com/tzapu/WiFiManager
#include <PubSubClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

//for LED status
#include <Ticker.h>
Ticker ticker;


#define RedLed 16
#define BlueLed 4
#define GreenLed 5
//--------------- NTP -SERVER  -------------------------------
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "co.pool.ntp.org", 3600, 60000);
//--------------- MQTT - STATUS -------------------------------
const char* mqttServer = "192.168.20.45" ;
const int mqttPort = 1883 ;
const char* mqttUser = "diego";
const char* mqttPassword ="1020785214";
const char* topico ="station5";
const char* client_name ="Station5";

byte willQoS = 1;

const char* willTopic = "station5/status";
const char* willMessage = "OFF";
boolean willRetain = true;

//--------------- Variables de conexión -------------------------------
int mqttCon=0;
int trys=0;
unsigned long check_wifi = 10000;
// Cliente ESP en el Broker mqtt
WiFiClient espClient;
PubSubClient client(espClient);
//--------------- Variables de payload -------------------------------
String sending_payload;
char buffer_tst[50];
unsigned long tst;
//---------------Battery Level ------------------------
const int analogInPin = A0; 
int battery_level = 0;  // value read from the pot

void callback(char* topic, byte* payload, unsigned int length) {
 
  for (int i = 0; i< length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println(" ");
}

// Reconexión al Broker MQTT
void reconnect(int trys) {
  // Loop until we're reconnected
  while (!client.connected()  && trys < 3 ) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(client_name, mqttUser, mqttPassword, willTopic, willQoS, willRetain, willMessage )) {
      Serial.println("connected");
      // Subscribe
      client.publish("station5/status","ON",true);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 3 seconds before retrying
      delay(3000);

    }
    trys ++;
    }
}

void tick()
{
  //toggle state
  digitalWrite(GreenLed, !digitalRead(GreenLed));     // set pin to the opposite state
}

//gets called when WiFiManager enters configuration mode
void configModeCallback (WiFiManager *myWiFiManager) {
  Serial.println("Entered config mode");
  Serial.println(WiFi.softAPIP());
  //if you used auto generated SSID, print it
  Serial.println(myWiFiManager->getConfigPortalSSID());
  //entered config mode, make led toggle faster
  ticker.attach(0.2, tick);
}



void setup() {
  WiFi.mode(WIFI_STA); // explicitly set mode, esp defaults to STA+AP
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  //set led pin as output
  pinMode(GreenLed, OUTPUT);
  pinMode(BlueLed, OUTPUT);
  pinMode(RedLed, OUTPUT);

  digitalWrite(GreenLed,LOW);
  digitalWrite(BlueLed,LOW);
  digitalWrite(RedLed,LOW);
  
  // start ticker with 0.5 because we start in AP mode and try to connect
  ticker.attach(0.6, tick);

  //WiFiManager
  //Local intialization. Once its business is done, there is no need to keep it around
  WiFiManager wm;
  //reset settings - for testing
  // wm.resetSettings();

  //set callback that gets called when connecting to previous WiFi fails, and enters Access Point mode
  wm.setAPCallback(configModeCallback);

  //fetches ssid and pass and tries to connect
  //if it does not connect it starts an access point with the specified name
  //here  "AutoConnectAP"
  //and goes into a blocking loop awaiting configuration
  if (!wm.autoConnect("Station 5 ","password")) {
    Serial.println("failed to connect and hit timeout");
    //reset and try again, or maybe put it to deep sleep
    ESP.restart();
    delay(1000);
  }

  //if you get here you have connected to the WiFi
  Serial.println("connected...yeey :)");
  timeClient.begin();
  ticker.detach();
  //keep LED on
  digitalWrite(GreenLed, LOW);
  
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  while (!client.connected()&& mqttCon==0 ) {
     Serial.println("Connecting to MQTT");
     if (client.connect(client_name, mqttUser, mqttPassword, willTopic, willQoS, willRetain, willMessage )) {
           client.publish("station5/status","ON",true);
      
          } else {
            Serial.print("failed with state ");
            Serial.print(client.state());
            delay(2000);
            mqttCon=1;
          }
        }
        client.subscribe(topico);
  
}

void loop() {

//   if(WiFi.status() == WL_CONNECTED && client.connected()){
//    
//    digitalWrite(GreenLed,LOW);
//    digitalWrite(BlueLed,LOW);
//    digitalWrite(RedLed,LOW);
//    delay(2000);
//    digitalWrite(GreenLed,HIGH);
//    digitalWrite(BlueLed,LOW);
//    digitalWrite(RedLed,HIGH);
//    delay(100);
//   }

  //publicar en el broker lo que venga por serial, adicionando tst y battery
   while(Serial.available() > 0 ){
    String payload = Serial.readString();

    timeClient.update();
    tst = timeClient.getEpochTime();
//    if(tst > 0xFFFFFFFFLL) {
//      sprintf(buffer_tst, "%lX%08lX", (unsigned long)(tst>>32), (unsigned long)(tst&0xFFFFFFFFULL));
//    } else {
//      sprintf(buffer_tst, "%lX", (unsigned long)tst);
//    }
     String myTst = String(tst);
     battery_level = analogRead(analogInPin);
 
    // print the readings in the Serial Monitor
    sending_payload = payload + "\"tst\":"+ myTst + "," + "\"bat\":"+ battery_level +"}";
    Serial.println(sending_payload);
  
    client.publish(topico,sending_payload.c_str());
  
  }
  // last will message y retain 
   
    
  if (WiFi.status() != WL_CONNECTED  && (millis() > check_wifi)){
    // Aqui no hay Wifi
    digitalWrite(GreenLed,LOW);
    digitalWrite(BlueLed,LOW);
    digitalWrite(RedLed,HIGH);

    if(WiFi.status() == WL_CONNECTED){
      Serial.println("We have internet again");
    }

    Serial.println("Reconnecting to WiFi...");
    WiFi.disconnect();
    WiFi.begin();
    
    check_wifi = millis() + 10000;
  }

  if (!client.connected()) {
    // Aqui no hay conexión con el Broker
    digitalWrite(GreenLed,LOW);
    digitalWrite(BlueLed,HIGH);
    digitalWrite(RedLed,HIGH);
    reconnect(trys);
  }

  client.loop();
  delay(10);
  
    digitalWrite(GreenLed,LOW);
    digitalWrite(BlueLed,LOW);
    digitalWrite(RedLed,LOW);
  

}
