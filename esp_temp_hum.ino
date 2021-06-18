#include <SimpleDHT.h>
#include <ArduinoJson.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

int pinDHT11 = 2; // GPIO2 of ESP8266
const char* ssid = "SSID";
const char* password = "PASSWD";

const char* mqtt_server = "xxxxx.cn";
const char* clientID = "ESP_01_A";          //连接mqtt用户名
const char *topic = "temp_hum";

int timeZone = 0; //东八区的时间
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "ntp1.aliyun.com", timeZone*3600, 60000);

WiFiClient espClient;
PubSubClient client(espClient);
SimpleDHT11 dht11(pinDHT11);

long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
  //pinMode(BUILTIN_LED, OUTPUT);     // 将BUILTIN_LED引脚初始化为输出
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  WiFi.begin(ssid, password);     // 我们从连接到WiFi网络开始
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println("WiFi connected");
}


///接收反馈
void callback(char* topic, byte* payload, unsigned int length) {
 Serial.print("Message arrived ["); Serial.print(topic);   Serial.print("] ");
 
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }  
}

void reconnect() {
  // 循环，直到我们重新连接
  while (!client.connected()) {
    
    if (client.connect(clientID)) {               //connected
      Serial.print("MQTT连接成功");                 // 连接mqtt成功
      client.subscribe(topic);               // 一旦连接，发布主题
    } else {
      delay(5000);                                 // 等待5秒再重试
    }
  }
}
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); 
    Serial.println(err);
    delay(1000);
    return;
  }
  timeClient.update();
  // json serialize
  DynamicJsonDocument data(256);
  data["_id"] = String(timeClient.getEpochTime());
  data["temp"] = String(temperature);
  data["hum"] = String(humidity);
  char json_string[256];
  serializeJson(data, json_string);
  //Serial.println(json_string);
  client.publish(topic, json_string, false);
  delay(2000);  
}
