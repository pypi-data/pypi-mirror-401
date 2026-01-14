import json

class Calibration:
    def __init__(self, filename="cal.json"):
        self.filename = filename
        
        # Lineaire Kalibratie (Fallback & Source)
        self.meas_v_m = 16.75
        self.meas_v_c = -35.8
        self.meas_i_m = 0.833
        self.meas_i_c = 0.0
        self.src_v_m = 1.0
        self.src_v_c = 0.0
        
        # Lookup Table (LUT) voor Voltage Meting
        # Lijst van [raw_adc, real_volts]
        self.meas_v_lut = []

        self.load()

    def load(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.meas_v_m = data.get("meas_v_m", self.meas_v_m)
                self.meas_v_c = data.get("meas_v_c", self.meas_v_c)
                self.meas_i_m = data.get("meas_i_m", self.meas_i_m)
                self.meas_i_c = data.get("meas_i_c", self.meas_i_c)
                self.src_v_m = data.get("src_v_m", self.src_v_m)
                self.src_v_c = data.get("src_v_c", self.src_v_c)
                # Laad tabel indien aanwezig
                self.meas_v_lut = data.get("meas_v_lut", [])
                # Sorteer voor de zekerheid op raw waarde
                self.meas_v_lut.sort(key=lambda x: x[0])
        except:
            print("Calibration file not found, using defaults.")

    def save(self):
        data = {
            "meas_v_m": self.meas_v_m, "meas_v_c": self.meas_v_c,
            "meas_i_m": self.meas_i_m, "meas_i_c": self.meas_i_c,
            "src_v_m": self.src_v_m, "src_v_c": self.src_v_c,
            "meas_v_lut": self.meas_v_lut
        }
        with open(self.filename, "w") as f:
            json.dump(data, f)

    # --- LUT MANAGEMENT ---
    def clear_lut(self):
        self.meas_v_lut = []

    def add_lut_point(self, raw, real):
        self.meas_v_lut.append([float(raw), float(real)])
        # Sorteer direct op raw ADC waarde (vereist voor interpolatie)
        self.meas_v_lut.sort(key=lambda x: x[0])

    def _interpolate(self, value, table):
        """Lineaire interpolatie door een tabel van [x, y] punten"""
        if not table:
            return None
        
        # Als waarde lager is dan het laagste punt: Extrapoleer met eerste segment
        if value <= table[0][0]:
            if len(table) > 1:
                x1, y1 = table[0]
                x2, y2 = table[1]
                slope = (y2 - y1) / (x2 - x1)
                return y1 + (value - x1) * slope
            else:
                return table[0][1]

        # Als waarde hoger is dan het hoogste punt: Extrapoleer met laatste segment
        if value >= table[-1][0]:
            if len(table) > 1:
                x1, y1 = table[-2]
                x2, y2 = table[-1]
                slope = (y2 - y1) / (x2 - x1)
                return y2 + (value - x2) * slope
            else:
                return table[-1][1]

        # Zoek het segment waar de waarde in valt
        for i in range(len(table) - 1):
            x1, y1 = table[i]
            x2, y2 = table[i+1]
            if x1 <= value <= x2:
                # Interpoleer
                fraction = (value - x1) / (x2 - x1)
                return y1 + fraction * (y2 - y1)
        
        return value # Should not happen

    # --- MEASURE ---
    def correct_voltage_read(self, adc_volts):
        # Gebruik Tabel als die bestaat (en meer dan 1 punt heeft)
        if len(self.meas_v_lut) > 1:
            return self._interpolate(adc_volts, self.meas_v_lut)
        
        # Fallback naar oude lineaire methode
        return (adc_volts * self.meas_v_m) + self.meas_v_c

    def correct_current_read(self, shunt_volts):
        # Current doen we voorlopig nog lineair (tenzij je hier ook een tabel voor wilt)
        return (shunt_volts * self.meas_i_m) + self.meas_i_c

    # --- SOURCE ---
    def correct_voltage_source(self, target_volts):
        # De DAC bleek in jouw data heel lineair, dus dit houden we simpel (formule)
        if self.src_v_m == 0: return target_volts
        return (target_volts - self.src_v_c) / self.src_v_m