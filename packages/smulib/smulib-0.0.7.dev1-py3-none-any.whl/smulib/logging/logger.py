from __future__ import annotations
import threading
import logging
import time
import os
import csv
from datetime import datetime, timezone, date
from typing import Dict, Any, Optional
from logging.handlers import RotatingFileHandler

from ..smu import SMU

CSV_HEADERS = ["timestamp_utc", "timestamp_epoch_ms", "voltage_v", "current_a"]

class SMULogger:
    def __init__(self,
                 smu: SMU | None,
                 data_request_interval: float = 1.0,
                 log_voltage: bool = True,
                 log_current: bool = True,
                 data_dir: str | None = None,
                 batch_size: int = 100,
                 batch_timeout: float = 0.5,
                 debug_log_dir: str | None = None,
                 debug_max_file_size_bytes: int = 5 * 1024 * 1024,
                 debug_backup_count: int = 5,
                 encoding: str = 'utf-8'):

        self.smu: SMU | None = smu
        self.data_request_interval = data_request_interval
        self.log_voltage = log_voltage
        self.log_current = log_current
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.encoding = encoding
        self.safe_port = str(getattr(self.smu, 'port', 'unknown')).replace('/', '_').replace('\\', '_')

        if data_dir is None: self.data_dir = os.path.join(os.path.abspath('.'), "data")
        else: self.data_dir = os.path.abspath(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)

        if not debug_log_dir: debug_log_dir = os.path.join(os.path.abspath('.'), "logs")
        self._debug_log_path = os.path.join(debug_log_dir, 'smu_debug.log')
        os.makedirs(debug_log_dir, exist_ok=True)

        handler = RotatingFileHandler(
            self._debug_log_path,
            maxBytes=debug_max_file_size_bytes,
            backupCount=debug_backup_count,
            encoding=self.encoding
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s\t- %(message)s')
        handler.setFormatter(formatter)

        self.debug_logger = logging.getLogger(f'smu.debug')
        self.debug_logger.propagate = False
        # remove old handlers if present
        for h in list(self.debug_logger.handlers):
            try:
                self.debug_logger.removeHandler(h)
            except Exception:
                pass
            try:
                h.close()
            except Exception:
                pass
        self.debug_logger.addHandler(handler)
        self.debug_logger.setLevel(logging.DEBUG)
        self.debug_logger.debug('RotatingFileHandler initialized: maxBytes=%d, backupCount=%d', debug_max_file_size_bytes, debug_backup_count)

        # threads and control
        self._poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._stop_event = threading.Event()
        self._running_event = threading.Event()
        self._settings_lock = threading.Lock()

    def start_data_logging(self) -> bool:
        if self.smu is None:
            self.debug_logger.debug('No SMU selected')
            return False
        self._stop_event.clear()
        self._running_event.clear()
        if not self._poll_thread.is_alive():
            self._poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
            self._poll_thread.start()
        self.debug_logger.debug('Data logging threads started')
        self._running_event.set()
        self.debug_logger.info('Data logging started')
        return True

    def stop_data_logging(self):
        # signal threads to stop
        self.debug_logger.info('Stopping data logging...')
        self._running_event.clear()
        self._stop_event.set()
        # wake threads
        self._running_event.set()
        # join threads
        try:
            self._poll_thread.join(timeout=2)
        except Exception:
            pass
        self.debug_logger.info('Data logging stopped')

    def close(self,):
        # close debug logger handlers
        handlers = list(self.debug_logger.handlers)
        for h in handlers:
            try:
                h.flush()
            except Exception:
                pass
            try:
                h.close()
            except Exception:
                pass
            try:
                self.debug_logger.removeHandler(h)
            except Exception:
                pass

    def set_logging_parameters(self, smu: Optional[SMU], log_voltage: Optional[bool] = None, log_current: Optional[bool] = None, data_request_interval: Optional[float] = None):
        with self._settings_lock:
            if smu is not None:
                self.smu = smu
            if log_voltage is not None:
                self.log_voltage = log_voltage
            if log_current is not None:
                self.log_current = log_current
            if data_request_interval is not None:
                self.data_request_interval = data_request_interval
        self.debug_logger.debug('Parameters updated: SMU, Log_V=%s Log_I=%s data_request_interval=%s', self.log_voltage, self.log_current, self.data_request_interval)

    def _poll_loop(self):

        def open_todays_file():
            nonlocal current_date, file_header, file_header, csv_writer
            if file_header:
                    try:
                        file_header.flush()
                    except Exception:
                        pass
                    try:
                        file_header.close()
                    except Exception:
                        pass

            current_date = datetime.now(timezone.utc).date()
            self._ensure_header_for_date(current_date)
            file_name = self._current_filename_for_date(current_date)
            file_header = open(file_name, 'a', encoding=self.encoding, newline='')
            csv_writer = csv.DictWriter(file_header, fieldnames=CSV_HEADERS)

        self.debug_logger.debug('Poller thread running')

        current_date = datetime.now(timezone.utc).date()
        self._ensure_header_for_date(current_date)
        file_name = self._current_filename_for_date(current_date)
        file_header = open(file_name, 'a', encoding=self.encoding, newline='')
        csv_writer = csv.DictWriter(file_header, fieldnames=CSV_HEADERS)

        while not self._stop_event.is_set():
            loop_start = time.monotonic()

            if datetime.now(timezone.utc).date() != current_date:
                open_todays_file()

            with self._settings_lock:
                log_v = self.log_voltage
                log_c = self.log_current
                data_request_interval = self.data_request_interval
            # build row
            now = datetime.now(timezone.utc)
            row: Dict[str, Any] = {
                CSV_HEADERS[0]: now.isoformat(),
                CSV_HEADERS[1]: int(now.timestamp() * 1000),
                CSV_HEADERS[2]: '',
                CSV_HEADERS[3]: ''
            }
            try:
                if log_v:
                    row['voltage_v'] = self.smu.measure_voltage()
                if log_c:
                    row['current_a'] = self.smu.measure_current()
            except Exception as e:
                self.debug_logger.exception('Error reading SMU: %s', e)
                # try:
                #     self.smu.reconnect()
                # except Exception:
                #     self.debug_logger.exception('Reconnect failed')
            try:
                csv_writer.writerow(row)
                file_header.flush()
            except Exception as e:
                pass

            elapsed = time.monotonic() - loop_start
            to_sleep = max(0.0, data_request_interval - elapsed)
            if self._stop_event.wait(to_sleep):
                break

        try:
            file_header.flush()
        except Exception:
            pass
        try:
            file_header.close()
        except Exception:
            pass

        self.debug_logger.debug('Poller thread exiting')

    def _current_filename_for_date(self, d: date) -> str:
        safe_port = str(getattr(self.smu, 'port', 'unknown')).replace('/', '_').replace('\\', '_')
        return os.path.join(self.data_dir, f"{safe_port}-{d.isoformat()}.csv")

    def _ensure_header_for_date(self, d: date):
        filename = self._current_filename_for_date(d)
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            if os.path.exists(filename) and os.path.getsize(filename) != 0: return
            with open(filename, 'a', encoding=self.encoding, newline='') as fh:
                writer = csv.DictWriter(fh, fieldnames=CSV_HEADERS)
                writer.writeheader()
                fh.flush()
        except Exception:
            self.debug_logger.exception('Failed to ensure header for %s', filename)

if __name__ == '__main__':
    print('SmuLogger module (queue-based) loaded.')