import random
from lib import ADS1115
from calibration import Calibration

class MeasureDriver:
    def __init__(self, ads: ADS1115, calibration: Calibration, avg_samples: int = 16, gain_diff: float = 1.0):
        self._ads: ADS1115 = ads
        self._cal = calibration
        self._gain_diff = gain_diff
        self._avg_samples = avg_samples      

    def _average(self, values):
        if not values: return 0.0
        return sum(values) / len(values)
    
    def _read_adc_voltage_avg(self, samples = None):
        """Returns the RAW voltage seen at the ADC pin (0-3.3V range approx)"""
        if samples is None:
            samples = self._avg_samples
        v_samples = []
        for _ in range(samples):
            # Channel 0 is measuring output voltage (scaled)
            raw = self._ads.read(rate=4, channel1=0)
            v_samples.append(self._ads.raw_to_v(raw))
        return self._average(v_samples)

    def measure_voltage(self) -> float:
        # 1. Get raw ADC voltage
        v_adc = self._read_adc_voltage_avg()
        # 2. Apply Calibration (Gain + Offset)
        smu_voltage = self._cal.correct_voltage_read(v_adc)
        return smu_voltage

    def _read_shunt_voltage_avg(self, samples = None):
        """Returns the RAW voltage across the shunt resistor"""
        if samples is None:
            samples = self._avg_samples
        v_samples = []
        for _ in range(samples):
            # Differential measure across shunt (Ch2 - Ch3)
            raw = self._ads.read(rate=4, channel1=2, channel2=3)
            # gain_diff accounts for any hardware op-amp gain on the shunt signal
            v_samples.append(self._ads.raw_to_v(raw) / self._gain_diff)
        return self._average(v_samples)

    def measure_current(self) -> float:
        # 1. Get raw voltage across shunt
        v_shunt_avg = self._read_shunt_voltage_avg()
        # 2. Apply Calibration (converts Volts -> Amps directly)
        current_A = self._cal.correct_current_read(v_shunt_avg)
        return current_A
    
    # Helper for calibration procedure (SCPI needs raw values)
    def get_raw_readings(self):
        return self._read_adc_voltage_avg(4), self._read_shunt_voltage_avg(4)


class MockMeasureDriver:
    def __init__(self):
        pass

    def measure_voltage(self) -> float:
        return (random.random() * 30) - 15 

    def measure_current(self) -> float:
        return (random.random() * 0.2) - 0.1