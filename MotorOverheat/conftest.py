import pytest
import yaml
from pathlib import Path

@pytest.fixture(scope="module")
def test_config():
    """Load test-specific configuration."""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

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