import logging
from paho_mqtt_helper.mqtt_helper import MQTTHelper
import time

# Enable logging to see paho_mqtt_helper messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize MQTT Helper with just certfile and keyfile
mqtt_client = MQTTHelper(
    # must match common name of certificate
    clientId="sap-ingestion",
    #mqtthost="mqtt.tf6073089-f620-457c-8b28-8da6929054fa.dev.cy.iot.sap",
    mqtthost="mqtt.mstoffel.eu-latest.cumulocity.com",
    mqttport=8883,
    topics="s/e,s/ds",
    ### could be removed if tls_insecure is True
    ca_certs="/opt/homebrew/etc/ca-certificates/cert.pem",
    certfile="../sap-ingestion.cert.pem",
    keyfile="../sap-ingestion.key.pem",
    tls_insecure=True
)

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")


def clear_alarm(alarm_type: str) -> str:
    print(f"Clearing alarm: {alarm_type}")
    payload = f"306,{alarm_type}"
    mqtt_client.publish("s/us", payload, qos=1)
    return payload

def motor_state(state: int) -> str:
    payload = f"200,motor-state,motor-state,{state},state"
    mqtt_client.publish("s/us", payload, qos=1)
    return payload


def maintenance_mode(mode: int) -> str:
    payload = f"200,maintenance-mode,maintenance-mode,{mode},state"
    mqtt_client.publish("s/us", payload, qos=1)
    return payload

def motor_overheated(overheated: int) -> str:
    payload = f"200,motor-overheated,motor-overheated,{overheated},state"
    mqtt_client.publish("s/us", payload, qos=1)
    return payload

# Alarm
def test_m1_ma0_oh1():
    print("Test: Motor On, Maintenance Off, Overheated On -> Alarm Expected")
    motor_state(1)
    time.sleep(1)
    maintenance_mode(0)
    time.sleep(1)
    motor_overheated(1)
    print("Press any key to continue...")
    input()
    
# No Alarm
def test_m0_ma1_oh1():
    print("Test: Motor Off, Maintenance On, Overheated On -> No Alarm Expected")
    motor_state(0)
    time.sleep(1)
    maintenance_mode(1)
    time.sleep(1)
    motor_overheated(1)
    print("Press any key to continue...")
    input()

# No Alarm
def test_m1_ma0_oh1_ma1():
    print("Test: Motor On, Maintenance Off, Overheated On, Maintenance On -> No Alarm Expected")
    motor_state(1)
    time.sleep(1)
    maintenance_mode(0)
    time.sleep(1)
    motor_overheated(1)
    time.sleep(1)
    maintenance_mode(1)
    print("Press any key to continue...")
    input()

# No Alarm
def test_m1_ma1_oh1_ma0():
    print("Test: Motor On, Maintenance On, Overheated On, Maintenance Off -> No Alarm Expected")
    motor_state(1)
    time.sleep(1)
    maintenance_mode(1)
    time.sleep(1)
    motor_overheated(1)
    time.sleep(1)
    maintenance_mode(0)
    print("Press any key to continue...")
    input()

# Connect and use
result = mqtt_client.connect(on_message)
if result == 0:
    print("Connected successfully")
    test_m1_ma0_oh1()
    time.sleep(2)
    clear_alarm("MotorOverheat")
    test_m0_ma1_oh1()
    time.sleep(2)
    clear_alarm("MotorOverheat")
    test_m1_ma0_oh1_ma1()
    time.sleep(2)
    clear_alarm("MotorOverheat")
    test_m1_ma1_oh1_ma0()
    time.sleep(2)
    clear_alarm("MotorOverheat")
    mqtt_client.disconnect()
else:
    print(f"Connection failed with result code: {result}")
