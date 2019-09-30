#include <ESP8266WiFi.h>
#include "DHT.h"
#include <PubSubClient.h>
#include "config.h"

#define DHTTYPE DHT22   // DHT 22

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
  
  server.begin();


  client.setServer(mqtt_server, 1883);

  // Printing the ESP IP address
  Serial.println(WiFi.localIP());

  h=0;
  f=0;
}

// runs over and over again
void loop() {
  // Listenning for new clients

  WiFiClient webClient = server.available();

  if (webClient) {
    while (client.connected()) {
      Serial.println("New Client");
      if (webClient.available()) {
        String line = webClient.readStringUntil('\r');
        Serial.print(line);
        if (line.length() == 1 && line[0] == '\n') {
          webClient.println("HTTP/1.1 200 OK");
          webClient.println("Content-type:text/html");
          webClient.println("Connection: close");
          webClient.println();
          webClient.println("<!DOCTYPE html><html>");
          snprintf (msg, 50, "%s", fahrenheitTemp);
          webClient.println("<head>Temp</head><body><h1>");
          webClient.println(msg);
          webClient.println("</h3></body></html>");
          break;
        }
      }
    }
  }

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 3000) {
    h = dht.readHumidity();
    f = dht.readTemperature(true);
    while (isnan(f)) {
      long now2 = millis();
      while (millis() - now2 < 100)
        ;
      h = dht.readHumidity();
      f = dht.readTemperature(true);
    }
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
