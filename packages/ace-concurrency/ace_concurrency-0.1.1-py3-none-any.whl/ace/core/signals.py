import asyncio
import psutil
import time
from dataclasses import dataclass
from typing import Dict
from threading import Lock


@dataclass
class SystemSignals:
    # Container for system health signals (percentages 0-100)
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    event_loop_lag_ms: float = 0.0
    queue_depth: int = 0
    kafka_lag: int = 0
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "event_loop_lag_ms": self.event_loop_lag_ms,
            "queue_depth": self.queue_depth,
            "kafka_lag": self.kafka_lag
        }


class SignalCollector:
    # Thread-safe system health signal collector
    
    def __init__(self, cpu_interval: float = 0.1):
        self.cpu_interval = cpu_interval
        self._lock = Lock()
        self._signals = SystemSignals()
        psutil.cpu_percent(interval=None)  # Initialize
    
    def collect_cpu_usage(self) -> float:
        return psutil.cpu_percent(interval=self.cpu_interval)
    
    def collect_memory_usage(self) -> float:
        return psutil.virtual_memory().percent
    
    async def collect_event_loop_lag(self) -> float:
        start = time.perf_counter()
        await asyncio.sleep(0)
        return (time.perf_counter() - start) * 1000
    
    def update_queue_depth(self, depth: int):
        with self._lock:
            self._signals.queue_depth = depth
    
    def update_kafka_lag(self, lag: int):
        with self._lock:
            self._signals.kafka_lag = lag
    
    async def collect_all_async(self) -> SystemSignals:
        cpu = self.collect_cpu_usage()
        memory = self.collect_memory_usage()
        event_loop_lag = await self.collect_event_loop_lag()
        
        with self._lock:
            queue_depth = self._signals.queue_depth
            kafka_lag = self._signals.kafka_lag
        
        return SystemSignals(
            cpu_percent=cpu,
            memory_percent=memory,
            event_loop_lag_ms=event_loop_lag,
            queue_depth=queue_depth,
            kafka_lag=kafka_lag
        )
    
    def collect_all_sync(self) -> SystemSignals:
        cpu = self.collect_cpu_usage()
        memory = self.collect_memory_usage()
        
        with self._lock:
            queue_depth = self._signals.queue_depth
            kafka_lag = self._signals.kafka_lag
        
        return SystemSignals(
            cpu_percent=cpu,
            memory_percent=memory,
            event_loop_lag_ms=0.0,
            queue_depth=queue_depth,
            kafka_lag=kafka_lag
        )
