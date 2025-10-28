from umqtt.simple import MQTTClient
from machine import Pin, ADC, PWM
import network
import ujson
import time

# MQTT Configuration 
MQTT_BROKER = "test.mosquitto.org"
CLIENT_ID = "sachin"
TOPIC_LED = "sachin/led1"
TOPIC_RGB = "sachin/rgb"
TOPIC_SENSOR = "sachin/sensor"

# Pin Configuration 
white_led = Pin(4, Pin.OUT)
gas_sensor = ADC(Pin(34))
gas_sensor.atten(ADC.ATTN_11DB)
pir_sensor = Pin(19, Pin.IN)

# RGB LED 
r_led = PWM(Pin(16))
g_led = PWM(Pin(17))
b_led = PWM(Pin(18))
for c in (r_led, g_led, b_led):
    c.freq(1000)

# Helper Functions
def set_rgb(r, g, b):
    r_led.duty(1023 - int(r * 4))
    g_led.duty(1023 - int(g * 4))
    b_led.duty(1023 - int(b * 4))

# WiFi Connection
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect("Wokwi-GUEST", "")
    print("Connecting to WiFi...", end="")
    while not wifi.isconnected():
        time.sleep(0.5)
        print(".", end="")
    print("\nWiFi connected")
    return True

# MQTT Message Handler
def message_callback(topic, msg):
    try:
        topic = topic.decode()
        msg = msg.decode().lower()
        print(f"Received message on {topic}: {msg}")

        if topic == TOPIC_LED:
            if msg == "on":
                white_led.value(1)
            elif msg == "off":
                white_led.value(0)

        elif topic == TOPIC_RGB:
            if msg == "red":
                set_rgb(255, 0, 0)
            elif msg == "green":
                set_rgb(0, 255, 0)
            elif msg == "blue":
                set_rgb(0, 0, 255)
            elif msg == "off":
                set_rgb(0, 0, 0)

    except Exception as e:
        print(f"Message Callback Error: {e}")

# MQTT Connection
def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=1883)
    client.set_callback(message_callback)
    client.connect()
    client.subscribe(TOPIC_LED)
    client.subscribe(TOPIC_RGB)
    print(f"Connected to MQTT broker: {MQTT_BROKER}")
    print(f"Subscribed to topics: {TOPIC_LED}, {TOPIC_RGB}")
    return client

# Publish Sensor Data
def publish_sensors(client):
    try:
        gas_value = gas_sensor.read()
        pir_value = pir_sensor.value()

        payload = ujson.dumps({
            "gas": gas_value,
            "motion": pir_value,
            "timestamp": time.time()
        })

        client.publish(TOPIC_SENSOR, payload)
        print(f"Published: {payload}")

    except Exception as e:
        print(f"Sensor Publish Error: {e}")

# Main Loop
def main():
    white_led.value(0)
    set_rgb(0, 0, 0)
        
    if not connect_wifi():
        print("WiFi connection failed!")
        return

    try:
        client = connect_mqtt()
    except Exception as e:
        print(f"MQTT Connection Failed: {e}")
        return

    while True:
        try:
            client.check_msg()
            publish_sensors(client)
            time.sleep(5)

        except KeyboardInterrupt:
            print("\nProgram stopped by user")
            break
        except Exception as e:
            print(f"Main Loop Error: {e}")
            time.sleep(2)

# Run Program
if __name__ == "__main__":
    main()