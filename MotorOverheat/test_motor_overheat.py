import pytest
import time


class TestMotorOverheat:
    """Tests for Motor Overheat alarm scenarios."""
    
    @pytest.fixture(autouse=True)
    def setup(self, test_config):
        """Automatically setup config for all tests.
        
        Args:
            test_config: Test-specific configuration fixture
        """
        self.config = test_config
        self.alarm_type = test_config['test']['alarm_type']
        self.operation_fragment = test_config['test']['operation_fragment']
    
    def sleep_between_commands(self):
        """Sleep for the configured time between commands."""
        time.sleep(self.config['test']['wait_between_commands'])
    
    def sleep_for_alarm(self):
        """Sleep for the configured time to wait for alarm."""
        time.sleep(self.config['test']['wait_for_alarm'])
    
    def verify_alarm_received_in_time(self, mqtt_ops, trigger_time):
        """Helper function to verify alarm was received within expected time range.
        
        Args:
            mqtt_ops: MQTT operations fixture
            trigger_time: Time when condition was triggered
            
        Returns:
            None (uses assertions)
        """
        alarm_received = mqtt_ops.check_operation(self.operation_fragment)
        
        response_time = mqtt_ops.get_operation_creation_time(trigger_time)
        if alarm_received:
            if response_time > self.config['test']['alarm_receive_timeout'] and response_time < self.config['test']['wait_for_alarm']:
                mqtt_ops.reset_operation(self.operation_fragment, True, f"Alarm received in {response_time:.3f}s")
                assert True, f"Alarm received as expected (response time: {response_time:.3f}s)"
            else:
                mqtt_ops.reset_operation(self.operation_fragment, False, f"Alarm received in {response_time:.3f}s outside expected range")
                pytest.fail(f"Alarm received but outside expected time range: {response_time:.3f}s")
        else:
            mqtt_ops.reset_operation(self.operation_fragment, False, "Alarm not received")
            pytest.fail("Alarm NOT received")
    
    def verify_no_alarm_received(self, mqtt_ops, trigger_time):
        """Helper function to verify no alarm was received.
        
        Args:
            mqtt_ops: MQTT operations fixture
            trigger_time: Time when condition was triggered
            
        Returns:
            None (uses assertions)
        """
        alarm_received = mqtt_ops.check_operation(self.operation_fragment)
        
        if alarm_received:
            response_time = mqtt_ops.get_operation_creation_time(trigger_time)
            print(f"\n❌ Unexpected alarm received after {response_time:.3f}s")
            mqtt_ops.reset_operation(self.operation_fragment, False, f"Unexpected alarm received in {response_time:.3f}s")
            pytest.fail("Alarm received when it shouldn't have been")
        else:
            print("\n✅ No alarm received as expected.")
            assert True, "No alarm as expected"
    
    def test_m1_ma0_oh1_alarm_expected(self, mqtt_ops):
        """Test: Motor On, Maintenance Off, Overheated On -> Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor On, Maintenance Off, Overheated On -> Alarm Expected")
        print("="*80)
        
        # Set up conditions
        mqtt_ops.motor_state(1)
        self.sleep_between_commands()
        
        mqtt_ops.maintenance_mode(0)
        self.sleep_between_commands()
        
        # Record time when overheat condition is triggered
        trigger_time = time.time()
        print(f"\n🔥 Triggering overheat condition at {trigger_time}")
        
        mqtt_ops.motor_overheated(1)
        self.sleep_for_alarm()
        
        # Check if alarm was received
        self.verify_alarm_received_in_time(mqtt_ops, trigger_time)

    def test_m0_ma1_oh1_no_alarm_expected(self, mqtt_ops):
        """Test: Motor Off, Maintenance On, Overheated On -> No Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor Off, Maintenance On, Overheated On -> No Alarm Expected")
        print("="*80)
        
        mqtt_ops.motor_state(0)
        self.sleep_between_commands()
        
        mqtt_ops.maintenance_mode(1)
        self.sleep_between_commands()
        
        trigger_time = time.time()
        print(f"\n🔥 Triggering overheat condition at {trigger_time}")
        
        mqtt_ops.motor_overheated(1)
        self.sleep_for_alarm()
        
        # Check that alarm was NOT received
        self.verify_no_alarm_received(mqtt_ops, trigger_time)
    
    def test_m1_ma0_oh1_ma1_no_alarm_expected(self, mqtt_ops):
        """Test: Motor On, Maintenance Off, Overheated On, Maintenance On -> No Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor On, Maintenance Off, Overheated On, Maintenance On -> No Alarm Expected")
        print("="*80)
        
        mqtt_ops.motor_state(1)
        self.sleep_between_commands()
        
        mqtt_ops.maintenance_mode(0)
        self.sleep_between_commands()
        
        trigger_time = time.time()
        print(f"\n🔥 Triggering overheat condition at {trigger_time}")
        
        mqtt_ops.motor_overheated(1)
        self.sleep_between_commands()
        
        print("\n🔧 Activating maintenance mode")
        mqtt_ops.maintenance_mode(1)
        self.sleep_for_alarm()
        
        # Check that alarm was NOT received
        self.verify_no_alarm_received(mqtt_ops, trigger_time)
    
    def test_m1_ma1_oh1_ma0_no_alarm_expected(self, mqtt_ops):
        """Test: Motor On, Maintenance On, Overheated On, Maintenance Off -> No Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor On, Maintenance On, Overheated On, Maintenance Off -> No Alarm Expected")
        print("="*80)
        
        mqtt_ops.motor_state(1)
        self.sleep_between_commands()
        
        mqtt_ops.maintenance_mode(1)
        self.sleep_between_commands()
        
        trigger_time = time.time()
        print(f"\n🔥 Triggering overheat condition at {trigger_time}")
        
        mqtt_ops.motor_overheated(1)
        self.sleep_between_commands()
        
        print("\n🔧 Deactivating maintenance mode")
        mqtt_ops.maintenance_mode(0)
        self.sleep_for_alarm()
        
        # Check that alarm was NOT received
        self.verify_no_alarm_received(mqtt_ops, trigger_time)

    def test_m1_ma0_oh1_oh1_oh1_alarm_expected(self, mqtt_ops):
        """Test: Motor On, Maintenance Off, Overheated On (repeated 3 times) ->  Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Motor On, Maintenance Off, Overheated On (repeated 3 times) -> Alarm Expected")
        print("="*80)
        
        mqtt_ops.motor_state(1)
        self.sleep_between_commands()
        
        mqtt_ops.maintenance_mode(0)
        self.sleep_between_commands()
        
        mqtt_ops.motor_overheated(1)
        self.sleep_between_commands()
        # Record time when overheat condition is triggered
        trigger_time = time.time()
        
        mqtt_ops.motor_overheated(1)
        self.sleep_between_commands()
        
        mqtt_ops.motor_overheated(1)
        self.sleep_for_alarm()
        
        # Check that alarm was received
        self.verify_alarm_received_in_time(mqtt_ops, trigger_time)