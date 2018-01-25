#include <ESP8266WiFi.h>
#include "DHT.h"
#include <PubSubClient.h>
#include "config.h"

#define DHTTYPE DHT11   // DHT 11

// This values are in config.h
/*const char* ssid = "";
const char* password = "";
const char* mqtt_server = "";*/


float h;
float f;


WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

// Web Server on port 80
WiFiServer server(80);

// DHT Sensor
const int DHTPin = 5;
// Initialize DHT sensor.
DHT dht(DHTPin, DHTTYPE);

// Temporary variables
static char fahrenheitTemp[7];
static char humidityTemp[7];

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      //client.publish("/sensors/dht11", "hello world");
      // ... and resubscribe
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// only runs once on boot
void setup() {
  // Initializing serial port for debugging purposes
  Serial.begin(115200);
  delay(10);

  dht.begin();

  // Connecting to WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");


  client.setServer(mqtt_server, 1883);

  // Printing the ESP IP address
  Serial.println(WiFi.localIP());

  h=0;
  f=0;
}

// runs over and over again
void loop() {
  // Listenning for new clients

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 30000) {
    int loops = 100;
    for(int i = 0; i < loops; i++){  
      h += dht.readHumidity();
      f += dht.readTemperature(true);
    }
    h = h / loops;
    f = f / loops;
    lastMsg = now;
    float hif = dht.computeHeatIndex(f, h);
    dtostrf(f, 6, 2, fahrenheitTemp);         
    dtostrf(h, 6, 2, humidityTemp);
    snprintf (msg, 50, "{\"temp\": %s, \"humidity\": %s}", fahrenheitTemp, humidityTemp);
    Serial.println(msg);
    client.publish("/sensors/garage/dht11", msg);
    h = 0;
    f = 0;
  }

}
