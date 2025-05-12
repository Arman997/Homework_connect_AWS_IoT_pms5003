import ssl
import json
import paho.mqtt.client as mqtt

aws_host = "d09530762c0nb5dceftxl-ats.iot.us-east-1.amazonaws.com"
aws_port = 8883
topic = "sensors/pms" 

ca_path = "/home/armanaristakesyan/Certificate/AmazonRootCA1.pem"
cert_path = "/home/armanaristakesyan/Certificate/accf-certificate.pem.crt"
key_path = "/home/armanaristakesyan/Certificate/accf-private.pem.key"

mqttc = mqtt.Client()

mqttc.tls_set(ca_certs=ca_path,
              certfile=cert_path,
              keyfile=key_path,
              tls_version=ssl.PROTOCOL_TLSv1_2)

mqttc.connect(aws_host, aws_port, keepalive=60)

message = {
    "test": 'Hello from raspberry pi 3 b'

        }


mqttc.publish(topic, json.dumps(message), qos=1)

mqttc.disconnect()
print("Message sent to AWS IoT.")

        
