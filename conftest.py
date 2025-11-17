import pytest
import yaml
import logging
import os
import warnings
from pathlib import Path
from dotenv import load_dotenv
from mqtt_operations import MQTTOperations

# Suppress deprecation warnings from third-party libraries
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@pytest.fixture(scope="session")
def config():
    """Load configuration from yaml file and environment variables."""
    config_path = Path(__file__).parent / "mqtt_config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Add MQTT configuration from environment variables
    config['mqtt'] = {
        'client_id': os.getenv('MQTT_CLIENT_ID'),
        'host': os.getenv('MQTT_HOST'),
        'port': int(os.getenv('MQTT_PORT', 8883)),
        'topics': os.getenv('MQTT_TOPICS'),
        'ca_certs': os.getenv('MQTT_CA_CERTS'),
        'certfile': os.getenv('MQTT_CERTFILE'),
        'keyfile': os.getenv('MQTT_KEYFILE'),
        'tls_insecure': os.getenv('MQTT_TLS_INSECURE', 'true').lower() == 'true'
    }
    
    # Validate required configuration
    required_keys = ['client_id', 'host', 'topics', 'ca_certs', 'certfile', 'keyfile']
    missing_keys = [key for key in required_keys if not config['mqtt'].get(key)]
    
    if missing_keys:
        raise ValueError(f"Missing required MQTT configuration: {', '.join(missing_keys)}")
    
    return config


@pytest.fixture(scope="session")
def mqtt_ops(config):
    """Create MQTT operations instance and connect."""
    ops = MQTTOperations(config['mqtt'])
    result = ops.connect()
    if result != 0:
        pytest.fail(f"Connection failed with result code: {result}")
    
    yield ops
    
    ops.disconnect()


@pytest.fixture(autouse=True)
def reset_alarm(mqtt_ops, config):
    """Reset alarm before each test."""
    mqtt_ops.received_operation.clear()
    mqtt_ops.clear_alarm_timestamps()
    mqtt_ops.clear_alarm("MotorOverheat")
    mqtt_ops.reset_operation("MotorOverheat", False, "Initial reset")
    
    yield
    
    # Cleanup after test
    mqtt_ops.clear_alarm("MotorOverheat")