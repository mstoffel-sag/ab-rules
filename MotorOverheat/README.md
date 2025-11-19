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

Edit `config.yaml` for timing and measurement parameters:

```yaml
test:
  # Timing parameters
  wait_for_alarm: 4 # Max time to wait for alarm (seconds)
  wait_between_commands: 1 # Delay between MQTT commands (seconds)
  wait_between_tests: 1 # Delay between test scenarios (seconds)
  alarm_receive_timeout: 3 # Min time before checking alarm (seconds)

  # Alarm configuration
  alarm_type: "MotorOverheat"
  operation_fragment: "MotorOverheat"

  # Measurement series and fragments
  motor_overheat_series: "motor-overheated"
  motor_overheat_fragment: "motor-overheated"
  maintenance_mode_fragment: "maintenance-mode"
  maintenance_mode_series: "maintenance-mode"
  motor_state_fragment: "motor-state"
  motor_state_series: "motor-state"
```

## Test Scenarios

### Positive (Alarm Expected)

1. **Motor ON + Maintenance OFF + Overheat ON** → Alarm after persistence threshold
2. **Multiple Overheat Signals** → Alarm after repeated signals

### Negative (No Alarm Expected)

1. **Motor OFF** → No alarm (motor not running)
2. **Maintenance Active Before Overheat** → No alarm (maintenance suppresses)
3. **Maintenance Activated After Overheat** → No alarm (maintenance suppresses existing condition)

## Measurement Values

The test uses the following measurement series and fragments (configurable in `config.yaml`):

- **Motor State**: `motor-state` (0=OFF, 1=ON)
- **Maintenance Mode**: `maintenance-mode` (0=OFF, 1=ON)
- **Motor Overheated**: `motor-overheated` (0=Normal, 1=Overheated)

## Setup

1. **Import Model**: Load `MotorOverheat.json` into Analytic Builder
2. **Activate Model**: Deploy and activate in Cumulocity
3. **Configure**: Adjust `config.yaml` timings and measurement names if needed
4. **Run Tests**: `pytest MotorOverheat/`

## Files

- `MotorOverheat.json`: Analytic Builder model definition
- `config.yaml`: Test-specific configuration
- `test_motor_overheat.py`: Test scenarios
