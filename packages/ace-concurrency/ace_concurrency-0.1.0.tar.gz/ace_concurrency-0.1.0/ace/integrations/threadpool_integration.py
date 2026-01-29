import threading
from typing import Callable, Optional
from concurrent.futures import Future
from ace.core.limiters import ACEThreadPoolLimiter
from ace.core.control import ACEController, AIMDConfig
from ace.core.signals import SignalCollector
from ace.core.logger import ACELogger


class ACEThreadPoolManager:
    """Manages thread pool concurrency with AIMD control loop"""
    
    def __init__(self, config: AIMDConfig, logger: Optional[ACELogger] = None, signal_collector: Optional[SignalCollector] = None):
        self.config = config
        self.logger = logger or ACELogger()
        self.signal_collector = signal_collector or SignalCollector()  # Monitors system health
        self.controller = ACEController(config, self.logger)  # AIMD decision engine
        self.limiter = ACEThreadPoolLimiter(initial_limit=config.initial_limit, logger=self.logger)  # Thread pool with dynamic sizing
        self._running = False
        self._control_thread: Optional[threading.Thread] = None  # Background control loop
    
    def _control_loop(self):
        """Runs every ~2s: collect signals → make AIMD decision → adjust thread pool size"""
        self.logger.log_info("ACE thread pool control loop started", {
            "initial_limit": self.config.initial_limit,
            "min_limit": self.config.min_limit,
            "max_limit": self.config.max_limit
        })
        
        import time
        
        while self._running:
            try:
                signals = self.signal_collector.collect_all_sync()  # Sync version for threads
                stats = self.limiter.get_stats()
                self.signal_collector.update_queue_depth(stats["queue_depth"])  # Track pending work
                new_limit = self.controller.adjust_limit(stats["limit"], stats["active"], signals)  # AIMD decision
                
                if new_limit != stats["limit"]:
                    self.limiter.set_limit(new_limit)  # Adjust thread pool size
                
                time.sleep(self.config.adjustment_interval_seconds)  # Default 2s
                
            except Exception as e:
                self.logger.log_error("control_loop_error", str(e))
                time.sleep(1)
    
    def start(self):
        if not self._running:
            self._running = True
            self._control_thread = threading.Thread(target=self._control_loop, daemon=True, name="ACE-ThreadPool-Control")
            self._control_thread.start()
    
    def stop(self, wait: bool = True):
        self._running = False
        if self._control_thread:
            self._control_thread.join(timeout=5)
        self.limiter.shutdown(wait=wait)
    
    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        return self.limiter.submit(fn, *args, **kwargs)
    
    def get_stats(self) -> dict:
        return self.limiter.get_stats()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
