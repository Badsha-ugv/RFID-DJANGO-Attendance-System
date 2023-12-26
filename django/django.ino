#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define SS_PIN D2 // Define the SS_PIN for RC522 module
#define RST_PIN D1 // Define the RST_PIN for RC522 module

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance

const char *ssid = "Neptune";
const char *password = "Passmerafi";
const char *serverAddress = "192.168.0.103";
const int serverPort = 8000; // Django server port

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String cardData = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      cardData += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      cardData += String(mfrc522.uid.uidByte[i], HEX);
    }

    Serial.println("Card ID: " + cardData);

    // Send data to the previous URL for the existing purpose
    sendCardDataToDjango("/api/receive_card_data/", cardData);

    // Send data to the new URL for the new purpose
    sendCardDataToDjango("/api/new_url_for_card_data/", cardData);

    delay(1000); // delay to avoid reading the same card multiple times
  }
}

void sendCardDataToDjango(const char *url, String cardData) {
  HTTPClient http;
  WiFiClient client;

  String fullUrl = "http://" + String(serverAddress) + ":" + String(serverPort) + url;
  Serial.println("Sending card data to Django: " + fullUrl);

  // Prepare the POST data
  String postData = "card_id=" + cardData;

  http.begin(client, fullUrl);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  // Add CSRF token to headers
  http.addHeader("Cookie", "csrftoken=your_csrf_token_here");

  // Send the POST request
  int httpResponseCode = http.POST(postData);

  if (httpResponseCode > 0) {
    Serial.print("Server response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Error on sending request. Response code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}
