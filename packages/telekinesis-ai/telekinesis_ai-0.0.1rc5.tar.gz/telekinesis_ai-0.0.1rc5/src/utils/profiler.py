import csv
import os
import time
import psutil
from datetime import datetime, timezone
from typing import Optional

class Profiler:
    """
    Profiles a single SDK request lifecycle.
    """

    def __init__(
        self,
        *,
        endpoint: str,
        method: str = "POST",
        enabled: bool = False,
    ):
        self.enabled = enabled
        self.endpoint = endpoint
        self.method = method

        self.process = psutil.Process()

        self.timings: dict[str, float] = {}
        self.sizes: dict[str, int] = {}

        self.start_wall = 0.0
        self.end_wall = 0.0
        self.start_cpu = 0.0
        self.end_cpu = 0.0
        self.start_mem = 0
        self.end_mem = 0

        self.output_dir = "profiling"
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.csv_path = os.path.join(self.output_dir, f"profile_{date}.csv")


        if self.enabled:
            os.makedirs(self.output_dir, exist_ok=True)

    # ---------- lifecycle ----------

    def start(self):
        if not self.enabled:
            return

        self.start_wall = time.perf_counter()
        self.start_cpu = time.process_time()
        self.start_mem = self.process.memory_info().rss

    def mark(self, name: str):
        if not self.enabled:
            return
        self.timings[name] = time.perf_counter()

    def end(self):
        if not self.enabled:
            return

        self.end_wall = time.perf_counter()
        self.end_cpu = time.process_time()
        self.end_mem = self.process.memory_info().rss

        self._write_csv()

    # ---------- payload ----------

    def add_sizes(self, *, request_bytes: int, response_bytes: int):
        if not self.enabled:
            return
        self.sizes["request_bytes"] = request_bytes
        self.sizes["response_bytes"] = response_bytes

    # ---------- internals ----------

    def _delta_ms(self, start: str, end: str) -> float:
        if start in self.timings and end in self.timings:
            return (self.timings[end] - self.timings[start]) * 1000
        return 0.0

    def _http_duration_s(self) -> float:
        if "http_start" in self.timings and "http_end" in self.timings:
            return self.timings["http_end"] - self.timings["http_start"]
        return 0.0


    # ---------- output ----------

    def _write_csv(self):

        http_duration_s = self._http_duration_s()

        request_mb = self.sizes.get("request_bytes", 0) / (1024 ** 2)
        response_mb = self.sizes.get("response_bytes", 0) / (1024 ** 2)

        upload_mbps = (
            (request_mb * 8) / http_duration_s
            if http_duration_s > 0
            else 0.0
        )

        download_mbps = (
            (response_mb * 8) / http_duration_s     
            if http_duration_s > 0
            else 0.0
        )

        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "endpoint": self.endpoint,
            "method": self.method,

            "total_time_ms": (self.end_wall - self.start_wall) * 1000,
            "cpu_time_ms": (self.end_cpu - self.start_cpu) * 1000,
            "memory_delta_mb": (self.end_mem - self.start_mem) / (1024**2),

            "build_request_time_ms": self._delta_ms("build_start", "build_end"),
            "http_time_ms": self._delta_ms("http_start", "http_end"),
            "parse_response_time_ms": self._delta_ms("parse_start", "parse_end"),

            "request_mb": request_mb,
            "response_mb": response_mb,

            "effective_upload_mbps": upload_mbps,
            "effective_download_mbps": download_mbps,
        }

        write_header = (
            not os.path.exists(self.csv_path)
            or os.path.getsize(self.csv_path) == 0
        )

        with open(self.csv_path, "a", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=row.keys(),
            )
            if write_header:
                writer.writeheader()
            writer.writerow(row)
