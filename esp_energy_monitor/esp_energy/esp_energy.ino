#include <PubSubClient.h>
#include <ESP8266WiFi.h>


const char* ssid = "NetworkBox-West";
const char* password = "sai1t0th3m00n";
const char* mqtt_server = "192.168.0.109";

WiFiClient espClient;
PubSubClient client(espClient);


int count = 0;
int trigger = 0;
int lastTrigger = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(D1, INPUT);
  Serial.begin(115200);

  
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to : ");
  Serial.println(ssid);
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  
  client.setServer(mqtt_server, 1883);

  
  digitalWrite(LED_BUILTIN, LOW);
}

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

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  trigger = digitalRead(D1);
  if (trigger != lastTrigger) {
    if (trigger == HIGH) {
      Serial.println("IR high");
      digitalWrite(LED_BUILTIN, HIGH);
      count++;
      Serial.print("Count: ");
      Serial.println(count);
      client.publish("/sensors/outside/energy", "tick");
    } else {
      Serial.println("IR low");
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
  delay(10);
  lastTrigger = trigger;
}
