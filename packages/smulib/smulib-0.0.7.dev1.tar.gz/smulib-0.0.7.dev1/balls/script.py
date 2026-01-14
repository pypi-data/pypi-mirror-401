from smulib import SMU, smu_script

@smu_script(name="Test")
def test(smu: SMU, v: float) -> dict[str, float]:
    smu.set_voltage(v)

    return {
        "v": smu.measure_voltage(),
        "a": smu.measure_current()
    }
