import logging
from paho_mqtt_helper.mqtt_helper import MQTTHelper
import time
import json

# Enable logging to see paho_mqtt_helper messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize MQTT Helper with just certfile and keyfile
mqtt_client = MQTTHelper(
    # must match common name of certificate
    clientId="sap-ingestion",
    mqtthost="mqtt.te0688583-6a69-467b-bde5-0cfe6568ad80.eu20.cy.iot.sap",
    #mqtthost="mqtt.tf6073089-f620-457c-8b28-8da6929054fa.dev.cy.iot.sap",
    #mqtthost="mqtt.mstoffel.eu-latest.cumulocity.com",
    mqttport=8883,
    topics="s/e,devicecontrol/notifications",
    ### could be removed if tls_insecure is True
    ca_certs="/opt/homebrew/etc/ca-certificates/cert.pem",
    certfile="../sap-ingestion.cert.pem",
    keyfile="../sap-ingestion.key.pem",
    tls_insecure=True
)


received_operation={}


def reset_operation(operation_fragment: str, result: bool, reason: str) -> None:
    print(f'resetting operation {operation_fragment} to {result} with reason \'{reason}\'')
    mqtt_client.publish("s/us", f"501,{operation_fragment}", qos=1)
    if result:
        mqtt_client.publish("s/us", f"503,{operation_fragment}", qos=1)
    else:
        mqtt_client.publish("s/us", f"502,{operation_fragment},{reason}", qos=1)
        

def check_operation(operation_fragment: str) -> bool:
    print(f'received_operation: {received_operation}')
    if operation_fragment in received_operation:
        print(f"Operation does contain '{operation_fragment}'")
        return True
    else:
        print(f"Operation does NOT contain '{operation_fragment}'")
        return False



def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")
    try:
        payload = json.loads(message.payload.decode())  
        received_operation.update(payload)
    except json.JSONDecodeError:
        print("Received message is not valid JSON")


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
    time.sleep(4)
    if check_operation("MotorOverheat"):
        print("Alarm received as expected.")
        reset_operation("MotorOverheat", True, "Alarm received")
    else:
        print("Alarm NOT received, test failed.")
        reset_operation("MotorOverheat", False, "Alarm not received")
    
    
    print("Press any key to continue...")
    input()
    clear_alarm("MotorOverheat")

    
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
    clear_alarm("MotorOverheat")
    reset_operation("MotorOverheat", False, "Initial reset")
    time.sleep(1)
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
