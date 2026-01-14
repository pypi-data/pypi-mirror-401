import utime
import math
from machine import I2C, Pin

DAC_RANGE_16 = 65535

# ERROR CODES
DAC8571_OK                = 0x00
DAC8571_I2C_ERROR         = 0x81
DAC8571_ADDRESS_ERROR     = 0x82
DAC8571_BUFFER_ERROR      = 0x83

# WRITE MODES
DAC8571_MODE_STORE_CACHE  = 0x00
DAC8571_MODE_NORMAL       = 0x01
DAC8571_MODE_WRITE_CACHE  = 0x02
DAC8571_MODE_BRCAST_0     = 0x03
DAC8571_MODE_BRCAST_1     = 0x04   # not supported
DAC8571_MODE_BRCAST_2     = 0x05   # not supported

# DAC VALUES (percentages)
DAC8571_VALUE_00          = 0x0000
DAC8571_VALUE_25          = 0x4000
DAC8571_VALUE_50          = 0x8000
DAC8571_VALUE_75          = 0xC000
DAC8571_VALUE_100         = 0xFFFF

# POWER DOWN MODES
DAC8571_PD_LOW_POWER      = 0x00
DAC8571_PD_FAST           = 0x01
DAC8571_PD_1_KOHM         = 0x02
DAC8571_PD_100_KOHM       = 0x03
DAC8571_PD_HI_Z           = 0x04

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class DAC8571:
    def __init__(self, i2c: I2C, address: int = 0x4C):
        self.__i2c = i2c
        self.__address = address
        self.__range = DAC_RANGE_16
        self.__dac = 0
        self.__control = 0
        self.__error = DAC8571_OK

        self.begin()

    def begin(self, value: int = DAC8571_VALUE_00) -> bool:
        if self.__address not in [0x4C, 0x4E]:
            self.__error = DAC8571_ADDRESS_ERROR
            return False

        if not self.is_connected():
            return False

        self.set_write_mode(DAC8571_MODE_NORMAL)

        return self.write(value)

    def is_connected(self) -> bool:
        try:
            self.__i2c.writeto(self.__address, b"")
            return True

        except OSError:
            return False

    def get_address(self) -> int:
        return self.__address

    def write_range(self, value: float, r_min: float, r_max: float):
        if value < r_min:
            value = r_min

        if value > r_max:
            value = r_max

        self.write(map_value(value, r_min, r_max, 0, self.__range))

    def write(self, value: int) -> bool:
        low_byte = value & 0xFF
        high_byte = value >> 8

        buf = bytes([self.__control, high_byte, low_byte])

        try:
            self.__i2c.writeto(self.__address, buf)

        except OSError:
            self.__error = DAC8571_I2C_ERROR
            return False

        self.__error = DAC8571_OK
        self.__dac = value

        return True

    def write_mapped(self, v: float, r: tuple[float, float], clamp: bool = True) -> bool:
        if clamp:
            if v < r[0]:
                v = r[0]

            if v > r[1]:
                v = r[1]

        v = int(map_value(v, r[0], r[1], 0, DAC_RANGE_16))

        return self.write(v)

    def read(self) -> int:
        data = self.__i2c.readfrom(self.__address, 3)

        high_byte = data[0]
        low_byte = data[1]

        self.__error = DAC8571_OK

        return high_byte * 256 + low_byte

    def set_percentage(self, percentage: float) -> bool:
        if percentage < 0:
            percentage = 0

        if percentage > 100:
            percentage = 100

        return self.write(int(percentage * 655.35))

    def get_percentage(self) -> float:
        return self.__dac * 0.0015259022

    def set_write_mode(self, mode: int = DAC8571_MODE_NORMAL) -> None:
        if mode > DAC8571_MODE_BRCAST_0:
            mode = DAC8571_MODE_NORMAL

        self.__control = mode << 4

    def get_write_mode(self) -> int:
        return (self.__control >> 4) & 0x03

    def power_down(self, pd_mode: int = DAC8571_PD_LOW_POWER) -> bool:
        pd_mask = {
            DAC8571_PD_LOW_POWER: 0x0000,
            DAC8571_PD_FAST: 0x2000,
            DAC8571_PD_1_KOHM: 0x4000,
            DAC8571_PD_100_KOHM: 0x8000,
            DAC8571_PD_HI_Z: 0xC000,
        }.get(pd_mode, 0x000)

        self.__control = (DAC8571_MODE_NORMAL << 4) + 0x01
        return self.write(pd_mask)

    def wake_up(self, value: int = DAC8571_VALUE_00) -> bool:
        self.set_write_mode(DAC8571_MODE_NORMAL)
        return self.write(value)

    def last_error(self) -> int:
        e = self.__error
        self.__error = DAC8571_OK
        return e


def dac_from_vout(vout):
    a = -0.00472
    b = 9.1228
    c = -(15.048 + vout)

    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        raise ValueError("No real solution")

    sqrt_disc = math.sqrt(discriminant)

    v1 = (-b + sqrt_disc) / (2*a)
    v2 = (-b - sqrt_disc) / (2*a)

    # choose solution within DAC range (0-3.3 V)
    for v in (v1, v2):
        if 0 <= v <= 3.3:
            return v

    raise ValueError("No solution in DAC range")

def frange(start, stop, step):
    x = start
    while x <= stop:
        yield round(x, 8)  # avoid tiny floating point errors
        x += step

if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400_000)

    print([hex(d) for d in i2c.scan()])

    v_dac = DAC8571(i2c, 0x4C)

    #v_out = dac_from_vout(17)

    v_dac.write_mapped(3.3, (0, 3.3))

    # for t_v in frange(-15, 16, 1):
    #     v_out = dac_from_vout(t_v)
    #
    #     v_dac.write_mapped(v_out, (0, 3.3))
    #
    #     d = v_dac.read()
    #
    #     print(f"Target: {t_v}, DAC: {v_out:.7f}, {d}")
    #
    #     utime.sleep(1)



