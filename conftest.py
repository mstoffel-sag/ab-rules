import pytest
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
def mqtt_config():
    """Load MQTT configuration from environment variables."""
    mqtt_config = {
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
    missing_keys = [key for key in required_keys if not mqtt_config.get(key)]
    
    if missing_keys:
        raise ValueError(f"Missing required MQTT configuration: {', '.join(missing_keys)}")
    
    return mqtt_config


@pytest.fixture(scope="session")
def mqtt_ops(mqtt_config):
    """Create MQTT operations instance and connect."""
    ops = MQTTOperations(mqtt_config)
    result = ops.connect()
    if result != 0:
        pytest.fail(f"Connection failed with result code: {result}")
    
    yield ops
    
    ops.disconnect()


@pytest.fixture(scope="module")
def test_config():
    """Load test-specific configuration."""
    config_path = Path(__file__).parent / "config.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def motor_ops():
    """Provide motor-specific helper functions."""
    return motor_helpers


@pytest.fixture(autouse=True)
def reset_alarm(mqtt_ops, test_config):
    """Reset alarm before each test using test-specific config."""
    alarm_type = test_config['test']['alarm_type']
    operation_fragment = test_config['test']['operation_fragment']
    
    mqtt_ops.received_operation.clear()
    mqtt_ops.clear_alarm_timestamps()
    mqtt_ops.clear_alarm(alarm_type)
    mqtt_ops.reset_operation(operation_fragment, False, "Initial reset")
    
    yield
    
    # Cleanup after test
    mqtt_ops.clear_alarm(alarm_type)