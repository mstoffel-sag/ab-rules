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

   - Before running tests, import the corresponding model JSON file (e.g., `MotorOverheat.json`) into Analytic Builder
   - Activate the model in Cumulocity IoT
   - Ensure the model is deployed and running

3. **Python**
   - Python 3.8 or higher
   - pip (Python package installer)

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ab-rules
```

### 2. Create Virtual Environment

Creating a virtual environment isolates the project dependencies from your system Python installation.

**On macOS/Linux:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**On Windows:**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**Verify activation:**
Your terminal prompt should now be prefixed with `(venv)`:

```
(venv) user@machine:~/ab-rules$
```

### 3. Install Dependencies

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

Create your environment configuration file:

```bash
cp .env.example .env
```

Edit `.env` with your MQTT credentials:

```bash
# Use your preferred editor
nano .env
# or
vim .env
# or
code .env  # VS Code
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

### 5. Place Certificates

Copy your MQTT certificates to the project directory:

```bash
cp /path/to/your-client.cert.pem .
cp /path/to/your-client.key.pem .
```

Update the certificate paths in `.env` if they differ.

### 6. Verify Setup

Test your configuration:

```bash
pytest --collect-only
```

This should list all available tests without running them.

## Deactivating Virtual Environment

When you're done working with the project:

```bash
deactivate
```

## Reactivating Virtual Environment

Next time you work on the project:

**On macOS/Linux:**

```bash
cd ab-rules
source venv/bin/activate
```

**On Windows:**

```bash
cd ab-rules
venv\Scripts\activate
```

## Configuration

### Environment Variables (.env)

Create a `.env` file in the top-level directory (use `.env.example` as template):

```bash
# MQTT Configuration
MQTT_CLIENT_ID=your-client-id
MQTT_HOST=your-tenant.cumulocity.com
MQTT_PORT=8883
MQTT_TOPICS=s/e,devicecontrol/notifications
MQTT_CA_CERTS=/path/to/ca-certificates/cert.pem
MQTT_CERTFILE=path/to/client.cert.pem
MQTT_KEYFILE=path/to/client.key.pem
MQTT_TLS_INSECURE=true
```

**Important:** The `.env` file contains sensitive credentials and should never be committed to version control. It's already included in `.gitignore`.

### Test Configuration (mqtt_config.yaml)

Edit `mqtt_config.yaml` for test timing parameters:

```yaml
test:
  wait_for_alarm: 4 # Seconds to wait for alarm to be received
  wait_between_commands: 1 # Seconds between MQTT commands
  wait_between_tests: 2 # Seconds between tests
```

## Project Structure

```
ab-rules/
├── README.md
├── pytest.ini                  # Pytest configuration
├── .env                        # MQTT credentials (not in git)
├── .env.example               # Template for .env file
├── mqtt_config.yaml           # Test timing configuration
├── requirements.txt           # Python dependencies
├── conftest.py               # Shared pytest fixtures
├── mqtt_operations.py        # MQTT helper functions
├── venv/                     # Virtual environment (not in git)
└── MotorOverheat/           # Motor Overheat test case
    ├── MotorOverheat.json   # Analytic Builder model definition
    └── test_motor_overheat.py  # Test scenarios
```

## Test Cases

### MotorOverheat

Tests an Analytic Builder model that triggers an alarm when a motor is running (not in maintenance mode) and becomes overheated.

**Analytic Builder Model Setup:**

1. Import `MotorOverheat/MotorOverheat.json` into Analytic Builder
2. The model should contain logic similar to:
   ```
   Input: motor-state measurement
   Input: maintenance-mode measurement
   Input: motor-overheated measurement
   Logic: IF motor-state = 1 AND maintenance-mode = 0 AND motor-overheated = 1
   Output: Create alarm "MotorOverheat"
   ```
3. Activate the model in Analytic Builder

**Test Scenarios:**

1. **test_m1_ma0_oh1_alarm_expected**

   - Motor State: ON (1)
   - Maintenance Mode: OFF (0)
   - Motor Overheated: ON (1)
   - **Expected:** Analytic Builder should trigger "MotorOverheat" alarm

2. **test_m0_ma1_oh1_no_alarm_expected**

   - Motor State: OFF (0)
   - Maintenance Mode: ON (1)
   - Motor Overheated: ON (1)
   - **Expected:** No alarm (motor is off, rule conditions not met)

3. **test_m1_ma0_oh1_ma1_no_alarm_expected**

   - Sequence: Motor ON → Maintenance OFF → Overheated ON → Maintenance ON
   - **Expected:** No alarm (maintenance mode activated after overheat condition)

4. **test_m1_ma1_oh1_ma0_no_alarm_expected**
   - Sequence: Motor ON → Maintenance ON → Overheated ON → Maintenance OFF
   - **Expected:** No alarm (overheat occurred during maintenance)

## Running Tests

**Ensure virtual environment is activated before running tests:**

```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### Run All Tests

```bash
pytest
```

### Run Tests for Specific Case

```bash
pytest MotorOverheat/
```

### Run Specific Test File

```bash
pytest MotorOverheat/test_motor_overheat.py
```

### Run Specific Test Method

```bash
pytest MotorOverheat/test_motor_overheat.py::TestMotorOverheat::test_m1_ma0_oh1_alarm_expected
```

### Stop on First Failure

```bash
pytest -x
```

### Verbose Output

```bash
pytest -v -s
```

### Generate HTML Report

```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

## How Tests Work

1. **Setup Phase (conftest.py)**

   - Loads test timing from `mqtt_config.yaml`
   - Loads MQTT credentials from `.env`
   - Establishes MQTT connection to Cumulocity
   - Clears any existing alarms before each test
   - Resets operation state

2. **Test Execution**

   - Publishes device measurements via MQTT using SmartREST protocol
   - Waits for configured time to allow Analytic Builder to process the data stream
   - Checks if expected alarm was received via MQTT subscription

3. **Assertion**

   - Verifies alarm was triggered (or not triggered) as expected by the Analytic Builder model
   - Reports operation success/failure to Cumulocity
   - Clears alarm for next test

4. **Cleanup**
   - Clears alarms after each test
   - Disconnects MQTT client after all tests complete

## SmartREST Messages

The tests use SmartREST 2.0 protocol to communicate with Cumulocity:

- `200,<fragment>,<series>,<value>,<type>` - Send measurement
- `306,<alarm-type>` - Clear alarm
- `501,<operation-id>` - Set operation to EXECUTING
- `502,<operation-id>,<reason>` - Set operation to FAILED
- `503,<operation-id>` - Set operation to SUCCESSFUL

## Adding New Test Cases

1. **Create Analytic Builder Model**

   - Design your model in Analytic Builder UI
   - Export the model as JSON

2. **Create Test Folder**

   - Create a new folder for your test case (e.g., `PressureAlert/`)
   - Add the exported Analytic Builder model JSON file

3. **Deploy Model**

   - Import the model into Analytic Builder
   - Activate the model

4. **Create Test File**
   - Create `test_<case_name>.py` in your folder
   - Use the `mqtt_ops` fixture from `conftest.py`
   - Write test methods following the existing pattern

Example:

```python
class TestPressureAlert:
    def test_high_pressure_alarm(self, mqtt_ops, config):
        # Send pressure measurement
        mqtt_ops.publish_measurement("pressure", 150)

        # Wait for Analytic Builder to process
        time.sleep(config['test']['wait_for_alarm'])

        # Check if alarm was triggered
        alarm_received = mqtt_ops.check_operation("PressureAlert")

        if alarm_received:
            mqtt_ops.reset_operation("PressureAlert", True, "Alarm received")
            assert True
        else:
            mqtt_ops.reset_operation("PressureAlert", False, "Alarm not received")
            pytest.fail("Alarm NOT received")
```

## Workflow

```
1. Design Model → 2. Export JSON → 3. Create Test Folder → 4. Import to AB
                                                                   ↓
                                                              5. Activate Model
                                                                   ↓
6. Configure .env ← Create from .env.example
     ↓
7. Run Tests ← Send Measurements ← MQTT Connection
     ↓
8. AB Processes Stream
     ↓
9. Check Alarm Received
     ↓
10. Assert & Report Results
```

## Troubleshooting

- **Connection Failed:**
  - Verify `.env` file exists and contains correct MQTT credentials
  - Check certificate paths in `.env`
  - Ensure certificates are in the correct location
- **Alarm Not Received:**
  - Verify Analytic Builder model is activated
  - Check model logs in Cumulocity
  - Ensure device measurements are reaching the platform
- **Timeout Issues:** Increase `wait_for_alarm` in `mqtt_config.yaml`
- **Test Failures:**
  - Review Analytic Builder model configuration
  - Check Cumulocity audit logs
  - Verify measurement fragments match model input blocks
- **Missing Configuration Error:**
  - Ensure all required variables are set in `.env`
  - Compare with `.env.example` to verify completeness

## Security Notes

- Never commit `.env` file to version control
- Keep certificates (`*.pem`, `*.key`, `*.crt`) out of version control
- Use `.env.example` as a template for team members
- Rotate credentials regularly
- Use different credentials for development and production

## Dependencies

- **pytest**: Testing framework
- **pyyaml**: YAML configuration parsing
- **paho-mqtt-helper**: MQTT client helper library for Cumulocity
- **python-dotenv**: Environment variable management

## Resources

- [Cumulocity IoT Documentation](https://cumulocity.com/docs/)
- [Analytic Builder Guide](https://cumulocity.com/guides/users-guide/analytics-builder/)
- [SmartREST 2.0 Protocol](https://cumulocity.com/guides/reference/smartrest-two/)

## License

[Your License Here]
