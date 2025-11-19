import pytest
import time


class TestMotorOverheat:
    """Tests for Motor Overheat alarm scenarios."""
    

    @pytest.fixture(autouse=True)
    def setup(self, test_config):
        """Automatically setup config and helpers for all tests.
        
        Args:
            test_config: Test-specific configuration fixture
            helpers: Generic send helper functions
        """
        self.config = test_config
        self.alarm_type = test_config['test']['alarm_type']
        self.operation_fragment = test_config['test']['operation_fragment']
    
    def send_motor_overheat(self, mqtt_ops, state: int):
        """Send motor overheat alarm."""
        print("\n🔥 Sending motor overheat alarm")
        mqtt_ops.mqtt_client.publish("s/us", f"200,{self.config['test']['motor_overheat_fragment']},{self.config['test']['motor_overheat_series']},{state}")
  
    def send_maintenance_mode(self, mqtt_ops, mode: int):
        """Send maintenance mode measurement."""
        print(f"\n🔧 Sending maintenance mode {mode}")
        mqtt_ops.mqtt_client.publish("s/us", f"200,{self.config['test']['maintenance_mode_fragment']},{self.config['test']['maintenance_mode_series']},{mode}")

    def send_motor_state(self, mqtt_ops, state: int):
        """Send motor state measurement."""
        print(f"\n⚙️ Sending motor state {state}")   
        mqtt_ops.mqtt_client.publish("s/us", f"200,{self.config['test']['motor_state_fragment']},{self.config['test']['motor_state_series']},{state}")
        

    def sleep_between_commands(self):
        """Sleep for the configured time between commands."""
        time.sleep(self.config['test']['wait_between_commands'])
    
    def sleep_for_alarm(self):
        """Sleep for the configured time to wait for alarm."""
        time.sleep(self.config['test']['wait_for_alarm'])
    
    def verify_alarm_received_in_time(self, mqtt_ops, trigger_time):
        """Helper function to verify alarm was received within expected time range."""
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
        """Helper function to verify no alarm was received."""
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
        self.send_motor_state(mqtt_ops, 1)
        self.sleep_between_commands()
        
        self.send_maintenance_mode(mqtt_ops, 0)
        self.sleep_between_commands()
        
        # Record time when overheat condition is triggered
        trigger_time = time.time()
        print(f"\n🔥 Triggering overheat condition at {trigger_time}")
        
        self.send_motor_overheat(mqtt_ops, 1)
        self.sleep_for_alarm()
        
        # Check if alarm was received
        self.verify_alarm_received_in_time(mqtt_ops, trigger_time)

    def test_m0_ma0_oh1_no_alarm(self, mqtt_ops):
        """Test: Motor Off, Maintenance Off, Overheated On -> No Alarm"""
        print("\n" + "="*80)
        print("Test: Motor Off, Maintenance Off, Overheated On -> No Alarm")
        print("="*80)
        
        # Set up conditions
        self.send_motor_state(mqtt_ops, 0)
        self.sleep_between_commands()
        
        self.send_maintenance_mode(mqtt_ops, 0)
        self.sleep_between_commands()
        
        trigger_time = time.time()
        self.send_motor_overheat(mqtt_ops, 1)
        self.sleep_for_alarm()
        
        # Verify no alarm
        self.verify_no_alarm_received(mqtt_ops, trigger_time)

    def test_m1_ma1_oh1_no_alarm(self, mqtt_ops):
        """Test: Motor On, Maintenance On, Overheated On -> No Alarm"""
        print("\n" + "="*80)
        print("Test: Motor On, Maintenance On, Overheated On -> No Alarm")
        print("="*80)
        
        # Set up conditions
        self.send_motor_state(mqtt_ops, 1)
        self.sleep_between_commands()
        
        self.send_maintenance_mode(mqtt_ops, 1)
        self.sleep_between_commands()
        
        trigger_time = time.time()
        self.send_motor_overheat(mqtt_ops, 1)
        self.sleep_for_alarm()
        
        # Verify no alarm
        self.verify_no_alarm_received(mqtt_ops, trigger_time)

    def test_m1_ma0_oh1_then_ma1_no_alarm(self, mqtt_ops):
        """Test: Motor On, Overheat triggered, then Maintenance On -> No Alarm"""
        print("\n" + "="*80)
        print("Test: Motor On, Overheat triggered, then Maintenance On -> No Alarm")
        print("="*80)
        
        # Set up initial conditions
        self.send_motor_state(mqtt_ops, 1)
        self.sleep_between_commands()
        
        self.send_maintenance_mode(mqtt_ops, 0)
        self.sleep_between_commands()
        
        trigger_time = time.time()
        self.send_motor_overheat(mqtt_ops, 1)
        self.sleep_between_commands()
        
        # Activate maintenance mode before alarm threshold
        self.send_maintenance_mode(mqtt_ops, 1)
        self.sleep_for_alarm()
        
        # Verify no alarm
        self.verify_no_alarm_received(mqtt_ops, trigger_time)

    def test_m1_ma0_oh1_multiple_signals_alarm_expected(self, mqtt_ops):
        """Test: Multiple overheat signals -> Alarm Expected"""
        print("\n" + "="*80)
        print("Test: Multiple overheat signals -> Alarm Expected")
        print("="*80)
        
        # Set up conditions
        self.send_motor_state(mqtt_ops, 1)
        self.sleep_between_commands()
        
        self.send_maintenance_mode(mqtt_ops, 0)
        self.sleep_between_commands()
        
        # Send multiple overheat signals
        trigger_time = time.time()
        for i in range(3):
            print(f"\n🔥 Sending overheat signal #{i+1}")
            self.send_motor_overheat(mqtt_ops, 1)
            time.sleep(0.5)
        
        self.sleep_for_alarm()
        
        # Check if alarm was received
        self.verify_alarm_received_in_time(mqtt_ops, trigger_time)