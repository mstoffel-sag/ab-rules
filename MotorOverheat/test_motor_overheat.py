import pytest
import time


class TestMotorOverheat:
    """Tests for Motor Overheat alarm scenarios."""
    
    def test_m1_ma0_oh1_alarm_expected(self, mqtt_ops, config):
        """Test: Motor On, Maintenance Off, Overheated On -> Alarm Expected"""
        print("Test: Motor On, Maintenance Off, Overheated On -> Alarm Expected")
        
        # Set up conditions
        mqtt_ops.motor_state(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(0)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_for_alarm'])
        
        # Check if alarm was received
        alarm_received = mqtt_ops.check_operation("MotorOverheat")
        
        if alarm_received:
            print("Alarm received as expected.")
            mqtt_ops.reset_operation("MotorOverheat", True, "Alarm received")
            assert True, "Alarm received as expected"
        else:
            print("Alarm NOT received, test failed.")
            mqtt_ops.reset_operation("MotorOverheat", False, "Alarm not received")
            pytest.fail("Alarm NOT received")
    
    def test_m0_ma1_oh1_no_alarm_expected(self, mqtt_ops, config):
        """Test: Motor Off, Maintenance On, Overheated On -> No Alarm Expected"""
        print("Test: Motor Off, Maintenance On, Overheated On -> No Alarm Expected")
        
        mqtt_ops.motor_state(0)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_for_alarm'])
        
        # Check that alarm was NOT received
        alarm_received = mqtt_ops.check_operation("MotorOverheat")
        
        if alarm_received:
            mqtt_ops.reset_operation("MotorOverheat", False, "Unexpected alarm received")
            pytest.fail("Alarm received when it shouldn't have been")
        else:
            print("No alarm received as expected.")
            assert True, "No alarm as expected"
    
    def test_m1_ma0_oh1_ma1_no_alarm_expected(self, mqtt_ops, config):
        """Test: Motor On, Maintenance Off, Overheated On, Maintenance On -> No Alarm Expected"""
        print("Test: Motor On, Maintenance Off, Overheated On, Maintenance On -> No Alarm Expected")
        
        mqtt_ops.motor_state(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(0)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(1)
        time.sleep(config['test']['wait_for_alarm'])
        
        # Check that alarm was NOT received
        alarm_received = mqtt_ops.check_operation("MotorOverheat")
        
        if alarm_received:
            mqtt_ops.reset_operation("MotorOverheat", False, "Unexpected alarm received")
            pytest.fail("Alarm received when it shouldn't have been")
        else:
            print("No alarm received as expected.")
            assert True, "No alarm as expected"
    
    def test_m1_ma1_oh1_ma0_no_alarm_expected(self, mqtt_ops, config):
        """Test: Motor On, Maintenance On, Overheated On, Maintenance Off -> No Alarm Expected"""
        print("Test: Motor On, Maintenance On, Overheated On, Maintenance Off -> No Alarm Expected")
        
        mqtt_ops.motor_state(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(0)
        time.sleep(config['test']['wait_for_alarm'])
        
        # Check that alarm was NOT received
        alarm_received = mqtt_ops.check_operation("MotorOverheat")
        
        if alarm_received:
            mqtt_ops.reset_operation("MotorOverheat", False, "Unexpected alarm received")
            pytest.fail("Alarm received when it shouldn't have been")
        else:
            print("No alarm received as expected.")
            assert True, "No alarm as expected"