import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt


LED_PIN = 17
BROKER_IP = "34.205.64.217"
TOPIC = "led/control"

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


def on_message(client, userdata, message):
    msg = message.payload.decode()
    print(f"message received: {msg}")
    if msg.lower() == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
    elif msg.lower() == "off":
        GPIO.output(LED_PIN, GPIO.LOW)



client = mqtt.Client()
client.on_message = on_message


client.connect(BROKER_IP, 1883)
client.subscribe(TOPIC)


try:
    print("Waiting for messages... Press Ctrl+C to exit")
    client.loop_forever()
except KeyboardInterrupt:
    print("the program has stopped")
finally:
    GPIO.cleanup()
