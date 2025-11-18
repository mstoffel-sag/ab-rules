"""Motor Overheat test-specific MQTT measurement helpers."""


def motor_state(mqtt_ops, state: int) -> str:
    """Send motor state measurement.
    
    Args:
        mqtt_ops: MQTTOperations instance
        state: 0 (OFF) or 1 (ON)
    
    Returns:
        The payload that was sent
    """
    payload = f"200,motor-state,motor-state,{state},state"
    mqtt_ops.mqtt_client.publish("s/us", payload, qos=1)
    return payload


def maintenance_mode(mqtt_ops, mode: int) -> str:
    """Send maintenance mode measurement.
    
    Args:
        mqtt_ops: MQTTOperations instance
        mode: 0 (OFF) or 1 (ON)
    
    Returns:
        The payload that was sent
    """
    payload = f"200,maintenance-mode,maintenance-mode,{mode},state"
    mqtt_ops.mqtt_client.publish("s/us", payload, qos=1)
    return payload


def motor_overheated(mqtt_ops, overheated: int) -> str:
    """Send motor overheated measurement.
    
    Args:
        mqtt_ops: MQTTOperations instance
        overheated: 0 (NOT overheated) or 1 (overheated)
    
    Returns:
        The payload that was sent
    """
    payload = f"200,motor-overheated,motor-overheated,{overheated},state"
    mqtt_ops.mqtt_client.publish("s/us", payload, qos=1)
    return payload