from smulib import SMU

smu = SMU("/dev/tty.usbserial-1440")

smu.set_voltage(12.0)
smu.set_current(0.100)

v = smu.measure_voltage()
i = smu.measure_current()

print(f"Voltage{v}, Current: {i}")
