# Motor Overheat Alarm System

## Overview

Tests an Analytic Builder model that triggers alarms when a motor overheats while running and not in maintenance mode.

## Alarm Logic

### Alarm Triggered When

All conditions must be met:

- ✅ Motor is **ON** (`motor_state = 1`)
- ✅ Maintenance mode is **OFF** (`maintenance_mode = 0`)
- ✅ Motor is **Overheated** (`motor_overheated = 1`)
- ✅ Overheat condition **persists** for configured threshold time

### No Alarm When

- ❌ Motor is **OFF**
- ❌ Maintenance mode is **ON**
- ❌ Motor is **NOT overheated**
- ❌ Overheat condition doesn't persist long enough

### Maintenance Mode Behavior

- Activated **after** overheat detected → alarm **suppressed**
- Deactivated **after** overheat occurred → alarm remains **suppressed**
- Must re-trigger overheat condition after maintenance ends

## Configuration

Edit `config.yaml` for timing parameters:

```yaml
test:
  wait_for_alarm: 4 # Max time to wait for alarm
  wait_between_commands: 1 # Delay between MQTT commands
  wait_between_tests: 1 # Delay between test scenarios
  alarm_receive_timeout: 3 # Min time before checking alarm
  alarm_type: "MotorOverheat"
  operation_fragment: "MotorOverheat"
```

## Test Scenarios

### Positive (Alarm Expected)

1. **Motor ON + Maintenance OFF + Overheat ON** → Alarm after persistence threshold
2. **Multiple Overheat Signals** → Alarm after repeated signals

### Negative (No Alarm Expected)

1. **Motor OFF** → No alarm (motor not running)
2. **Maintenance Active Before Overheat** → No alarm (maintenance suppresses)
3. **Maintenance Activated After Overheat** → No alarm (maintenance suppresses existing condition)

## Setup

1. **Import Model**: Load `MotorOverheat.json` into Analytic Builder
2. **Activate Model**: Deploy and activate in Cumulocity
3. **Configure**: Adjust `config.yaml` timings if needed
4. **Run Tests**: `pytest MotorOverheat/`

## Files

- `MotorOverheat.json`: Analytic Builder model definition
- `config.yaml`: Test-specific configuration
- `conftest.py`: Test fixtures and setup/teardown
- `test_motor_overheat.py`: Test scenarios
