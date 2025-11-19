# AB Rules - Analytic Builder Rules Testing for Cumulocity IoT

This project contains automated tests for Analytic Builder rules deployed in Cumulocity IoT platform using pytest and MQTT.

## Overview

The tests verify that Analytic Builder models (streaming analytics rules) are working correctly by sending device measurements via MQTT and validating that alarms and notifications are triggered as expected based on the configured rules.

**Analytic Builder** is Cumulocity's streaming analytics solution that allows you to create real-time data processing workflows by connecting blocks in a visual model.

## Prerequisites

1. **Cumulocity IoT Setup**

   - Access to a Cumulocity IoT tenant with Analytic Builder enabled
   - MQTT credentials (client certificate and key)
   - Device registered in Cumulocity

2. **Analytic Builder Model Deployment**

   - Before running tests, import the corresponding model JSON file into Analytic Builder
   - Activate the model in Cumulocity IoT
   - Ensure the model is deployed and running

3. **Python**
   - Python 3.8 or higher
   - pip (Python package installer)

## Setup

### 1. Clone and Install

```bash
git clone <repository-url>
cd ab-rules

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your MQTT credentials
```

Example `.env` content:

```bash
MQTT_CLIENT_ID=your-client-id
MQTT_HOST=your-tenant.cumulocity.com
MQTT_PORT=8883
MQTT_TOPICS=s/e,devicecontrol/notifications
MQTT_CA_CERTS=/path/to/ca-certificates/cert.pem
MQTT_CERTFILE=path/to/client.cert.pem
MQTT_KEYFILE=path/to/client.key.pem
MQTT_TLS_INSECURE=true
```

## Project Structure

```
ab-rules/
├── README.md
├── pytest.ini
├── .env                        # MQTT credentials (not in git)
├── .env.example               # Template for .env file
├── requirements.txt
├── conftest.py                # Global pytest fixtures
├── mqtt_operations.py         # MQTT helper functions
└── MotorOverheat/             # Test case directory
    ├── MotorOverheat.json     # Analytic Builder model
    ├── README.md              # Test case documentation
    ├── config.yaml            # Test-specific configuration
    └── test_motor_overheat.py # Test implementation
```

## Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run specific test case
pytest MotorOverheat/

# Run with verbose output
pytest -v -s

# Stop on first failure
pytest -x
```

## How Tests Work

1. **Setup**: Loads global MQTT config from `.env` and test-specific config from each test case's `config.yaml`
2. **Execution**: Publishes measurements via MQTT, waits for Analytic Builder to process
3. **Verification**: Checks if expected alarms were triggered
4. **Cleanup**: Clears alarms and resets state

## Adding New Test Cases

1. **Create Test Directory**: `mkdir NewTestCase/`
2. **Add Model JSON**: Export from Analytic Builder and place in directory
3. **Create config.yaml**: Define test-specific timings and parameters
4. **Create test file**: Write test scenarios using `mqtt_ops` fixture (e.g., `test_new_case.py`)
5. **Add README.md**: Document the test case logic and scenarios

Example `config.yaml`:

```yaml
test:
  wait_for_alarm: 4
  wait_between_commands: 1
  alarm_type: "YourAlarmType"
  operation_fragment: "YourOperation"
```

## Security Notes

- Never commit `.env` file or certificates to version control
- Use `.env.example` as a template
- Rotate credentials regularly

## Dependencies

- **pytest**: Testing framework
- **pyyaml**: YAML configuration parsing
- **paho-mqtt-helper**: MQTT client for Cumulocity
- **python-dotenv**: Environment variable management

## Resources

- [Cumulocity IoT Documentation](https://cumulocity.com/docs/)
- [Analytic Builder Guide](https://cumulocity.com/guides/users-guide/analytics-builder/)
- [SmartREST 2.0 Protocol](https://cumulocity.com/guides/reference/smartrest-two/)
