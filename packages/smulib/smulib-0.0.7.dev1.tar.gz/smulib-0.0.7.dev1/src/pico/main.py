import uasyncio as asyncio
from primitives import Queue
import _thread
from machine import I2C, Pin
import utime

from lib import DAC8571, ADS1115
from sourcing import SourceDriver
from measuring import MeasureDriver
from scpi import SCPIProcessor
from state import State
from serial_helper import read_line, write_line
from calibration import Calibration

# CONFIG
VOLTAGE_RANGE = (-15, 15)
CURRENT_RANGE = (-0.1, 0.1)

# PINS
I2C_SDA = Pin(16)
I2C_SCL = Pin(17)
p15_dac_enable = Pin(15, Pin.OUT)

i2c = I2C(0, scl=I2C_SCL, sda=I2C_SDA, freq=400_000)
i2c_lock = _thread.allocate_lock()

# Initialize Hardware
voltage_dac = DAC8571(i2c, 0x4C)
ads = ADS1115(i2c, 0x48, gain=1)

# Initialize Calibration (loads from cal.json)
cal = Calibration()

source_driver = SourceDriver(
    voltage_dac,
    calibration=cal,
    v_range=VOLTAGE_RANGE,
)

measure_driver = MeasureDriver(ads, calibration=cal)

# Default Start State: Output OFF, 0V
state = State(v_range=VOLTAGE_RANGE)

scpi = SCPIProcessor()

cmd_queue = Queue(16)


@scpi.query("CMDS")
def get_commands(_):
    return str(scpi.list_commands())

# --- SOURCE COMMANDS ---
@scpi.command(":SOUR:VOLT")
def set_source_voltage(params):
    try:
        v = float(params[0])
        with state.lock:
            state.source_voltage = v
    except ValueError:
        pass

@scpi.query(":SOUR:VOLT")
def get_source_voltage(_):
    with state.lock:
        return state.source_voltage

@scpi.command(":SOUR:CURR")
def set_source_current(params):
    try:
        a = float(params[0])
        with state.lock:
            state.source_current = a
    except ValueError:
        pass

@scpi.query(":SOUR:CURR")
def get_source_current(_):
    with state.lock:
        return state.source_current

# --- LIMITS ---
@scpi.command(":SOUR:CURR:LIM")
def set_current_limit(params):
    try:
        a_lim = float(params[0])
        with state.lock:
            state.current_limit = abs(a_lim)
    except ValueError:
        pass

@scpi.query(":SOUR:CURR:LIM")
def get_current_limit(_):
    with state.lock:
        return state.current_limit

@scpi.command(":SOUR:VOLT:LIM")
def set_voltage_limit(params):
    try:
        v_lim = float(params[0])
        with state.lock:
            state.voltage_limit = abs(v_lim)
    except ValueError:
        pass

@scpi.query(":SOUR:VOLT:LIM")
def get_voltage_limit(_):
    with state.lock:
        return state.voltage_limit

# --- MEASUREMENTS ---
@scpi.query(":MEAS:VOLT")
def measure_voltage(_):
    with state.lock:
        return state.measured_voltage

@scpi.query(":MEAS:CURR")
def measure_current(_):
    with state.lock:
        return state.measured_current

# --- OUTPUT ---
@scpi.command(":OUTP")
def set_output(params):
    if not params:
        return
    arg = str(params[0]).upper()
    enable = (arg == "ON" or arg == "1" or arg == "TRUE")
    with state.lock:
        state.output_enabled = enable

# --- CALIBRATION ---
@scpi.query(":CAL:RAW")
def get_raw_calibration_data(_):
    with i2c_lock:
        raw_v, raw_i = measure_driver.get_raw_readings()
    return f"{raw_v},{raw_i}"

@scpi.command(":CAL:SOUR:VOLT")
def set_cal_sour_volt(params):
    try:
        cal.src_v_m = float(params[0])
        cal.src_v_c = float(params[1])
    except: return "ERR"

# --- LUT COMMANDS ---
@scpi.command(":CAL:LUT:CLEAR")
def clear_lut_cal(_):
    cal.clear_lut()
    return "Cleared"

@scpi.command(":CAL:LUT:ADD")
def add_lut_cal(params):
    # Verwacht: :CAL:LUT:ADD <raw_adc>,<real_volts>
    try:
        raw = float(params[0])
        real = float(params[1])
        cal.add_lut_point(raw, real)
    except: return "ERR"

@scpi.command(":CAL:SAVE")
def save_calibration(_):
    cal.save()
    return "OK"

@scpi.command(":CAL:RESET")
def reset_calibration(_):
    cal.meas_v_m = 1.0; cal.meas_v_c = 0.0
    cal.meas_i_m = 1.0; cal.meas_i_c = 0.0
    cal.src_v_m = 1.0; cal.src_v_c = 0.0
    cal.clear_lut()
    return "Reset"

# --- TASKS ---
def adjust_self():
    with state.lock:
        enabled = state.output_enabled
        mode = state.func
        v_set = state.source_voltage

    if enabled:
        p15_dac_enable.value(1)
        v_out = 0.0
        if mode == "VOLT":
            v_out = v_set
        with i2c_lock:
            source_driver.set_voltage(v_out)
    else:
        p15_dac_enable.value(0)
        with i2c_lock:
            source_driver.set_voltage(0.0)

def task_measurement():
    while True:
        with i2c_lock:
            v = measure_driver.measure_voltage()
            i = measure_driver.measure_current()
        with state.lock:
            state.measured_voltage = v
            state.measured_current = i
        adjust_self()
        utime.sleep_ms(20)

async def task_usb_reader():
    while True:
        line = read_line()
        if line:
            res = scpi.handle_line(line.strip())
            if res:
                write_line(res)
        await asyncio.sleep_ms(10)

def main():
    p15_dac_enable.value(0)
    with i2c_lock:
        source_driver.set_voltage(0.0)
    _thread.start_new_thread(task_measurement, ())
    loop = asyncio.get_event_loop()
    loop.create_task(task_usb_reader())
    loop.run_forever()

if __name__ == "__main__":
    main()