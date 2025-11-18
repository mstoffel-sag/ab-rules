# Motor Overheat Alarm System

## Overview

This project implements and tests an alarm system for motor overheat conditions. The system monitors motor temperature and triggers alarms based on specific conditions while respecting maintenance mode settings.

## Alarm Logic

### When Alarm is Triggered

The Motor Overheat alarm is triggered when **ALL** of the following conditions are met:

- ✅ Motor is **ON** (`motor_state = 1`)
- ✅ Maintenance mode is **OFF** (`maintenance_mode = 0`)
- ✅ Motor is **Overheated** (`motor_overheated = 1`)
- ✅ The overheat condition **persists** for a specific duration (configured threshold time)

**Note:** The alarm will only trigger after the overheat condition has been continuously present for the required time period. Brief or transient overheat signals that don't persist will not trigger an alarm.

### When Alarm is NOT Triggered

The alarm will **NOT** be triggered in any of the following scenarios:

- ❌ Motor is **OFF** (regardless of other conditions)
- ❌ Maintenance mode is **ON** (regardless of other conditions)
- ❌ Motor is **NOT overheated**
- ❌ Overheat condition does **NOT persist** long enough (below threshold duration)

### Maintenance Mode Behavior

- When maintenance mode is activated **after** an overheat condition is detected, the alarm is **suppressed**
- When maintenance mode is deactivated **after** an overheat condition occurs, the alarm remains **suppressed** (overheat condition must be re-triggered)
- Maintenance mode takes precedence over alarm conditions

## Test Scenarios

### Positive Tests (Alarm Expected)

1. **Motor ON + Maintenance OFF + Overheat ON**
   - Expected: Alarm triggered within configured time window after persistence threshold is met
2. **Multiple Overheat Signals**
   - Motor ON + Maintenance OFF + Overheat ON (repeated 3 times)
   - Expected: Alarm triggered after repeated signals meet persistence threshold

### Negative Tests (No Alarm Expected)

1. **Motor OFF**

   - Motor OFF + Maintenance ON + Overheat ON
   - Expected: No alarm (motor not running)

2. **Maintenance Mode Active Before Overheat**

   - Motor ON + Maintenance ON + Overheat ON + Maintenance OFF
   - Expected: No alarm (maintenance mode was active when condition occurred)

3. **Maintenance Mode Activated After Overheat**
   - Motor ON + Maintenance OFF + Overheat ON + Maintenance ON
   - Expected: No alarm (maintenance mode suppresses existing condition)

## Configuration

The system uses timing configurations defined in `../config.yaml`:

- `alarm_receive_timeout`: Minimum time to wait before checking for alarm (persistence threshold)
- `wait_for_alarm`: Maximum time to wait for alarm response
- `wait_between_commands`: Delay between MQTT commands
