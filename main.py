import serial
import time
import json
import ssl
import paho.mqtt.client as mqtt

# AWS IoT Core MQTT configuration
aws_host = "d09530762c0nb5dceftxl-ats.iot.us-east-1.amazonaws.com"
aws_port = 8883
topic = "sensors/pms"

# Certificate paths
ca_path = "/home/armanaristakesyan/Certificate/AmazonRootCA1.pem"
cert_path = "/home/armanaristakesyan/Certificate/accf-certificate.pem.crt"
key_path = "/home/armanaristakesyan/Certificate/accf-private.pem.key"

# Setup MQTT client with TLS
mqttc = mqtt.Client()  # Without client_id

mqttc.tls_set(ca_certs=ca_path,
              certfile=cert_path,
              keyfile=key_path,
              tls_version=ssl.PROTOCOL_TLSv1_2)

mqttc.connect(aws_host, aws_port, keepalive=60)

# Open PMS5003 serial port
try:
    ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=2)
    print("PMS5003 connected. Reading data...")
except Exception as e:
    print("Failed to connect to PMS5003:", e)
    exit(1)

# Read once and send data
byte = ser.read(1)
if byte == b'\x42':
    if ser.read(1) == b'\x4d':
        frame = ser.read(30)
        if len(frame) == 30:
            pm1_0  = frame[0] << 8 | frame[1]
            pm2_5  = frame[2] << 8 | frame[3]
            pm10   = frame[4] << 8 | frame[5]

            payload = {
                "pm1_0": pm1_0,
                "pm2_5": pm2_5,
                "pm10": pm10,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }

            mqttc.publish(topic, json.dumps(payload), qos=1)
            print("Sent to AWS IoT:", payload)
        else:
            print("Incomplete data frame.")
mqttc.disconnect()




