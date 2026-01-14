from lib import DAC8571
from calibration import Calibration

class SourceDriver:
    def __init__(self, v_dac: DAC8571, calibration: Calibration, v_range: tuple[float, float] = (-15, 15)):
        self._v_dac = v_dac
        self._v_range = v_range
        self._cal = calibration

    def set_voltage(self, v: float):
        # 1. Check logical bounds (what the user WANTS)
        if not (self._v_range[0] <= v <= self._v_range[1]):
            # Optional: Clamp instead of error?
            pass # ValueError("Voltage out of range")

        # 2. Apply Calibration to find the 'Pre-distorted' value
        # e.g. if we want 10V but output is usually 10% low, we ask for 11V.
        v_corrected = self._cal.correct_voltage_source(v)

        # 3. Write the corrected value to the DAC driver
        # The DAC driver maps this virtual voltage to 0-65535
        self._v_dac.write_mapped(v_corrected, self._v_range)


class MockSourceDriver:
    def __init__(self, v_range: tuple[float, float] = (-15, 15)):
        self._v_range = v_range

    def set_voltage(self, v: float):
        return