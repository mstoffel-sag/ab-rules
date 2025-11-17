import pytest
import time


class TestMotorOverheat:
    """Tests for Motor Overheat alarm scenarios."""
    
    def test_m1_ma0_oh1_alarm_expected(self, mqtt_ops, config):
        """Test: Motor On, Maintenance Off, Overheated On -> Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor On, Maintenance Off, Overheated On -> Alarm Expected")
        print("="*80)
        
        # Set up conditions
        mqtt_ops.motor_state(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(0)
        time.sleep(config['test']['wait_between_commands'])
        
        # Record time when overheat condition is triggered
        trigger_time = time.time()
        print(f"\n🔥 Triggering overheat condition at {trigger_time}")
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_for_alarm'])
        
        # Check if alarm was received
        alarm_received = mqtt_ops.check_operation("MotorOverheat")
        
        response_time = mqtt_ops.get_alarm_response_time("MotorOverheat", trigger_time)
        if alarm_received and response_time > config['test']['alarm_receive_timeout'] and response_time < config['test']['wait_for_alarm']:
            # Calculate response time
            
            print(f"\n✅ Alarm received as expected.")
            print(f"⏱️  Response time: {response_time:.3f} seconds")
            
            mqtt_ops.reset_operation("MotorOverheat", True, f"Alarm received in {response_time:.3f}s")
            assert True, f"Alarm received as expected (response time: {response_time:.3f}s)"
        else:
            print("\n❌ Alarm NOT received, test failed.")
            mqtt_ops.reset_operation("MotorOverheat", False, "Alarm not received")
            pytest.fail("Alarm NOT received")
    
    def test_m0_ma1_oh1_no_alarm_expected(self, mqtt_ops, config):
        """Test: Motor Off, Maintenance On, Overheated On -> No Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor Off, Maintenance On, Overheated On -> No Alarm Expected")
        print("="*80)
        
        mqtt_ops.motor_state(0)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(1)
        time.sleep(config['test']['wait_between_commands'])
        
        trigger_time = time.time()
        print(f"\n🔥 Triggering overheat condition at {trigger_time}")
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_for_alarm'])
        
        # Check that alarm was NOT received
        alarm_received = mqtt_ops.check_operation("MotorOverheat")
        
        if alarm_received:
            response_time = mqtt_ops.get_alarm_response_time("MotorOverheat", trigger_time)
            print(f"\n❌ Unexpected alarm received after {response_time:.3f}s")
            mqtt_ops.reset_operation("MotorOverheat", False, f"Unexpected alarm received in {response_time:.3f}s")
            pytest.fail("Alarm received when it shouldn't have been")
        else:
            print("\n✅ No alarm received as expected.")
            assert True, "No alarm as expected"
    
    def test_m1_ma0_oh1_ma1_no_alarm_expected(self, mqtt_ops, config):
        """Test: Motor On, Maintenance Off, Overheated On, Maintenance On -> No Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor On, Maintenance Off, Overheated On, Maintenance On -> No Alarm Expected")
        print("="*80)
        
        mqtt_ops.motor_state(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(0)
        time.sleep(config['test']['wait_between_commands'])
        
        trigger_time = time.time()
        print(f"\n🔥 Triggering overheat condition at {trigger_time}")
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_between_commands'])
        
        print("\n🔧 Activating maintenance mode")
        mqtt_ops.maintenance_mode(1)
        time.sleep(config['test']['wait_for_alarm'])
        
        # Check that alarm was NOT received
        alarm_received = mqtt_ops.check_operation("MotorOverheat")
        
        if alarm_received:
            response_time = mqtt_ops.get_alarm_response_time("MotorOverheat", trigger_time)
            print(f"\n❌ Unexpected alarm received after {response_time:.3f}s")
            mqtt_ops.reset_operation("MotorOverheat", False, f"Unexpected alarm received in {response_time:.3f}s")
            pytest.fail("Alarm received when it shouldn't have been")
        else:
            print("\n✅ No alarm received as expected.")
            assert True, "No alarm as expected"
    
    def test_m1_ma1_oh1_ma0_no_alarm_expected(self, mqtt_ops, config):
        """Test: Motor On, Maintenance On, Overheated On, Maintenance Off -> No Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor On, Maintenance On, Overheated On, Maintenance Off -> No Alarm Expected")
        print("="*80)
        
        mqtt_ops.motor_state(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(1)
        time.sleep(config['test']['wait_between_commands'])
        
        trigger_time = time.time()
        print(f"\n🔥 Triggering overheat condition at {trigger_time}")
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_between_commands'])
        
        print("\n🔧 Deactivating maintenance mode")
        mqtt_ops.maintenance_mode(0)
        time.sleep(config['test']['wait_for_alarm'])
        
        # Check that alarm was NOT received
        alarm_received = mqtt_ops.check_operation("MotorOverheat")
        
        if alarm_received:
            response_time = mqtt_ops.get_alarm_response_time("MotorOverheat", trigger_time)
            print(f"\n❌ Unexpected alarm received after {response_time:.3f}s")
            mqtt_ops.reset_operation("MotorOverheat", False, f"Unexpected alarm received in {response_time:.3f}s")
            pytest.fail("Alarm received when it shouldn't have been")
        else:
            print("\n✅ No alarm received as expected.")
            assert True, "No alarm as expected"

    def test_m1_ma0_oh1_oh1_oh1_alarm_expected(self, mqtt_ops, config):
        """Test: Motor On, Maintenance Off, Overheated On (repeated 3 times) ->  Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor On, Maintenance Off, Overheated On (repeated 3 times) -> Alarm Expected")
        print("="*80)
        
        mqtt_ops.motor_state(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.maintenance_mode(0)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_between_commands'])
        # Record time when overheat condition is triggered
        trigger_time = time.time()
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_between_commands'])
        
        mqtt_ops.motor_overheated(1)
        time.sleep(config['test']['wait_for_alarm'])
        
        # Check that alarm was received
        alarm_received = mqtt_ops.check_operation("MotorOverheat")
        
        if alarm_received:
            response_time = mqtt_ops.get_alarm_response_time("MotorOverheat", trigger_time)
            if response_time > config['test']['alarm_receive_timeout'] and response_time < config['test']['wait_for_alarm']:

                print(f"\n✅ Alarm received as expected in time.")
                print(f"⏱️  Response time: {response_time:.3f} seconds")
            
                mqtt_ops.reset_operation("MotorOverheat", True, f"Alarm received in {response_time:.3f}s")
                assert True, f"Alarm received as expected (response time: {response_time:.3f}s)"
            else:
                print(f"\n❌ Alarm received but outside expected time range: {response_time:.3f}s")
                mqtt_ops.reset_operation("MotorOverheat", False, f"Alarm received in {response_time:.3f}s outside expected range")
                pytest.fail(f"Alarm received but outside expected time range: {response_time:.3f}s")
        else:
            print("\n❌ Alarm NOT received, test failed.")
            mqtt_ops.reset_operation("MotorOverheat", False, "Alarm not received")
            pytest.fail("Alarm NOT received")