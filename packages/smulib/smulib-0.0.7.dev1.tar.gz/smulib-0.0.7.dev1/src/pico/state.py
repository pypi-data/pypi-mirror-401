import _thread
from typing import Literal
from lib import PID

class State:
    def __init__(self, v_range: tuple[float, float]):
        self.lock = _thread.allocate_lock()

        # CHANGED: Default to False (OFF) for safety
        self.output_enabled: bool = False
        
        self.func: Literal["VOLT", "CURR"] = "VOLT"
        
        # CHANGED: Default to 0.0V for safety
        self.source_voltage: float = 0.0
        self.source_current: float = 0.0
        
        self.voltage_limit: float = 0.0
        self.current_limit: float = 0.0

        self.measured_voltage: float = 0.0
        self.measured_current: float = 0.0
        
        self.voltage_pid: PID = PID(
            Kp=0.5,
            Ki=0.5,
            Kd=0.0,
            setpoint=0.0, # Changed from 7.5 to 0.0
            output_limits=v_range,
            sample_time=1,
            scale="ms"
        )