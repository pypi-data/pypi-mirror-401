import time

from smulib import SMU, smu_script

@smu_script(name="I-V Sweep")
def sweep(smu: SMU) -> dict[float, float]:
    smu.set_voltage(0.0)

    v = 0.0

    res = {}

    for _ in range(100):
        v += 0.01
        smu.set_voltage(v)
        print(v)

        time.sleep(0.1)

        a = smu.measure_current()
        res[v] = a

    smu.set_voltage(0.0)

    return res
