import importlib.util
import inspect
import os
import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import serial
from serial.tools import list_ports

from .base import SMUBase
from .scripting import SMUScript, SMUScriptCallable, SMUScriptParameter

_LOG = logging.getLogger(__name__)

class SMU(SMUBase):
    def __init__(self, port: str, baudrate: int = 115200, timeout: float | None = 1.0):
        self.__port = port
        self.__baudrate = baudrate
        self.__timeout = timeout
        self._serial = None
        self._connect_attempts: int = 0
        self._last_connect_time: float = 0.0
        self.max_backoff: float = 3.0
        self.initial_backoff: float = 0.1

        self._serial_lock = threading.Lock()

        try:
            self.connect()
        except Exception:
            _LOG.exception("Initial connect failed for %s", port)
            self._serial = None

    @property
    def port(self) -> str:
        return self.__port

    def connect(self) -> None:
        with self._serial_lock:
            try:
                self._serial = serial.Serial(port=self.__port, baudrate=self.__baudrate, timeout=self.__timeout)
                self._connect_attempts = 0
                self._last_connect_time = time.monotonic()
                _LOG.debug("Connected to SMU on %s", self.__port)
            except Exception as e:
                _LOG.exception("Failed to open serial port %s", self.__port)
                self._serial = None
                raise IOError(f"Could not open port {self.__port}: {e}") from e

    def disconnect(self) -> None:
        with self._serial_lock:
            if self._serial is not None:
                try:
                    self._serial.close()
                except Exception:
                    _LOG.exception("Error while closing serial port")
                finally:
                    self._serial = None
                    _LOG.debug("Disconnected from %s", self.__port)

    def reconnect(self) -> None:
        with self._serial_lock:
            backoff = self.initial_backoff
            attempts = 0
            while True:
                try:
                    self.connect()
                    return
                except IOError:
                    attempts += 1
                    if backoff > self.max_backoff:
                        raise IOError(f"Failed to reconnect after {attempts} attempts") from None
                    _LOG.warning("Reconnect attempt %d failed, backing off %.2fs", attempts, backoff)
                    time.sleep(backoff)
                    backoff *= 2

    def __write(self, command: str) -> None:
        # with self._serial_lock:
        if self._serial is None:
            raise IOError("Serial not connected")
        self._serial.write((command + "\n").encode())

    def __read(self, command: str) -> str:
        # with self._serial_lock:
        if self._serial is None:
            raise IOError("Serial not connected")
        self.__write(command)
        raw = self._serial.readline()
        if isinstance(raw, bytes):
            raw = raw.decode(errors='ignore')
        return str(raw).strip()

    def set_output(self, out: bool) -> None:
        with self._serial_lock:
            self.__write(f":OUTP {'ON' if out else 'OFF'}")

    def set_voltage(self, v: float) -> None:
        with self._serial_lock:
            self.__write(f":SOUR:VOLT {float(v)}")

    def set_current(self, i: float) -> None:
        with self._serial_lock:
            self.__write(f":SOUR:CURR {float(i)}")

    def get_voltage(self) -> float:
        with self._serial_lock:
            return float(self.__read(":SOUR:VOLT?"))

    def get_current(self) -> float:
        with self._serial_lock:
            return float(self.__read(":SOUR:CURR?"))

    def set_voltage_limit(self, v: float) -> None:
        with self._serial_lock:
            self.__write(f":SOUR:VOLT:LIM {float(v)}")

    def set_current_limit(self, i: float) -> None:
        with self._serial_lock:
            self.__write(f":SOUR:CURR:LIM {float(i)}")

    def voltage_limit(self) -> float:
        with self._serial_lock:
            return float(self.__read(":SOUR:VOLT:LIM?"))

    def current_limit(self) -> float:
        with self._serial_lock:
            return float(self.__read(":SOUR:CURR:LIM?"))

    def measure_voltage(self) -> float:
        with self._serial_lock:
            return float(self.__read(":MEAS:VOLT?"))

    def measure_current(self) -> float:
        with self._serial_lock:
            return float(self.__read(":MEAS:CURR?"))

    def run_script(self, script: SMUScriptCallable, *args, **kwargs) -> Any | list | dict:
        return script(self, *args, **kwargs)
    
    @staticmethod
    def discover_scripts(scripts_dir: str) -> list[SMUScript]:
        path = os.path.join(os.getcwd(), scripts_dir)
        files = [f for f in os.listdir(path) if f.endswith(".py")]

        results = []

        for f in files:
            module_name = path[:-3]
            full_path = os.path.join(path, f)
            spec = importlib.util.spec_from_file_location(module_name, full_path)

            if not spec or not spec.loader:
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, func in inspect.getmembers(module, inspect.isfunction):
                if not getattr(func, "_is_smu_script", False):
                    continue

                script_name = getattr(func, "_smu_script_name", "Unknown")

                params = [
                    SMUScriptParameter(
                        p.name,
                        p.annotation,
                        p.default if p.default != inspect.Parameter.empty else None
                    ) for p in inspect.signature(func).parameters.values()
                ]

                if len(params) == 0 \
                   or len([p for p in params if getattr(p.value_type, "__name__") == "SMU"]) != 1 \
                   or getattr(params[0].value_type, "__name__") != "SMU":
                    continue

                results.append(SMUScript(script_name, params, func))

        return results

    @staticmethod
    def discover_ports() -> dict[str, str]:
        """Return a dict of {device: IDN response} for all PicoSMU devices."""
        ports = list_ports.comports()
        result = {}

        # Use a thread pool to check ports in parallel
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(SMU._check_port, port.device): port.device for port in ports}

            for future in as_completed(futures):
                device = futures[future]
                try:
                    idn = future.result()
                    if idn:
                        result[device] = idn
                except Exception:
                    pass  # ignore serial exceptions

        return result

    @staticmethod
    def _check_port(port: str) -> str | None:
        """Check a single port for a valid PicoSMU response to *IDN?"""
        try:
            conn = serial.Serial(port, baudrate=115200, timeout=0.5)
            time.sleep(0.2)  # let device reset if needed
            conn.reset_input_buffer()
            conn.reset_output_buffer()
            conn.write(b"*IDN?\r\n")

            # Read with a manual timeout
            end = time.time() + 0.5
            res = b""
            while time.time() < end:
                if conn.in_waiting:
                    res += conn.read(conn.in_waiting)
                    if b"\n" in res or b"\r" in res:
                        break
                else:
                    time.sleep(0.01)
            conn.close()

            res_str = res.decode(errors="ignore").strip()
            parts = res_str.split(",")
            if len(parts) == 4 and parts[1] == "PicoSMU":
                return res_str
            return None
        except serial.SerialException:
            return None

if __name__ == "__main__":
    print(SMU.discover_scripts("balls"))