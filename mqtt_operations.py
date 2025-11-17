import datetime
import json
import time

from paho_mqtt_helper.mqtt_helper import MQTTHelper


class MQTTOperations:
    def __init__(self, config: dict):
        self.received_operation = {}
        self.alarm_timestamps = 0.0  # Track when alarms are received
        self.mqtt_client = MQTTHelper(
            clientId=config['client_id'],
            mqtthost=config['host'],
            mqttport=config['port'],
            topics=config['topics'],
            ca_certs=config['ca_certs'],
            certfile=config['certfile'],
            keyfile=config['keyfile'],
            tls_insecure=config['tls_insecure']
        )
    
    def on_message(self, client, userdata, message):
        print(f"Received message: {message.payload.decode()}")
        try:
            payload = json.loads(message.payload.decode())
            self.received_operation.update(payload)
            
            # Record timestamp when alarm is received
            self.alarm_timestamps = datetime.datetime.fromisoformat(payload["delivery"]["time"]).timestamp()
            print(f"Alarm timestamp recorded: {self.alarm_timestamps}")
            
        except json.JSONDecodeError:
            print("Received message is not valid JSON")
    
    def connect(self):
        return self.mqtt_client.connect(self.on_message)
    
    def disconnect(self):
        self.mqtt_client.disconnect()
    
    def reset_operation(self, operation_fragment: str, result: bool, reason: str) -> None:
        print(f'resetting operation {operation_fragment} to {result} with reason \'{reason}\'')
        self.mqtt_client.publish("s/us", f"501,{operation_fragment}", qos=1)
        if result:
            self.mqtt_client.publish("s/us", f"503,{operation_fragment}", qos=1)
        else:
            self.mqtt_client.publish("s/us", f"502,{operation_fragment},{reason}", qos=1)
    
    def check_operation(self, operation_fragment: str) -> bool:
        print(f'received_operation: {self.received_operation}')
        if operation_fragment in self.received_operation:
            print(f"Operation does contain '{operation_fragment}'")
            return True
        else:
            print(f"Operation does NOT contain '{operation_fragment}'")
            return False
    
    def get_alarm_response_time(self, operation_fragment: str, trigger_time: float) -> float:
        """Calculate the time between trigger and alarm receipt."""
        response_time = self.alarm_timestamps - trigger_time
        print(f"Alarm response time for '{operation_fragment}': {response_time:.3f} seconds")
        return response_time
    
    def clear_alarm_timestamps(self):
        """Clear alarm timestamp tracking."""
        self.alarm_timestamps = 0.0
    
    def clear_alarm(self, alarm_type: str) -> str:
        print(f"Clearing alarm: {alarm_type}")
        payload = f"306,{alarm_type}"
        self.mqtt_client.publish("s/us", payload, qos=1)
        return payload
    
    def motor_state(self, state: int) -> str:
        payload = f"200,motor-state,motor-state,{state},state"
        self.mqtt_client.publish("s/us", payload, qos=1)
        return payload
    
    def maintenance_mode(self, mode: int) -> str:
        payload = f"200,maintenance-mode,maintenance-mode,{mode},state"
        self.mqtt_client.publish("s/us", payload, qos=1)
        return payload
    
    def motor_overheated(self, overheated: int) -> str:
        payload = f"200,motor-overheated,motor-overheated,{overheated},state"
        self.mqtt_client.publish("s/us", payload, qos=1)
        return payload