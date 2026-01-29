import asyncio
from typing import Callable, Any, Optional
from ace.core.limiters import ACESemaphore
from ace.core.control import ACEController, AIMDConfig
from ace.core.signals import SignalCollector
from ace.core.logger import ACELogger


class ACEAsyncioManager:
    """Manages async task concurrency with AIMD control loop"""
    
    def __init__(self, config: AIMDConfig, logger: Optional[ACELogger] = None, signal_collector: Optional[SignalCollector] = None):
        self.config = config
        self.logger = logger or ACELogger()
        self.signal_collector = signal_collector or SignalCollector()  # Monitors CPU, memory, etc.
        self.controller = ACEController(config, self.logger)  # AIMD decision engine
        self.semaphore = ACESemaphore(initial_limit=config.initial_limit, logger=self.logger)  # Enforces concurrency limit
        self._control_task: Optional[asyncio.Task] = None  # Background control loop
        self._running = False
    
    async def _control_loop(self):
        """Runs every ~2s: collect signals → make AIMD decision → adjust limit"""
        self.logger.log_info("ACE asyncio control loop started", {
            "initial_limit": self.config.initial_limit,
            "min_limit": self.config.min_limit,
            "max_limit": self.config.max_limit
        })
        
        while self._running:
            try:
                signals = await self.signal_collector.collect_all_async()  # Get CPU, memory, etc.
                stats = self.semaphore.get_stats()  # Get current limit, active tasks
                new_limit = self.controller.adjust_limit(stats["limit"], stats["active"], signals)  # AIMD decision
                
                if new_limit != stats["limit"]:
                    await self.semaphore.set_limit(new_limit)  # Apply new concurrency limit
                
                await asyncio.sleep(self.config.adjustment_interval_seconds)  # Default 2s
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.log_error("control_loop_error", str(e))
                await asyncio.sleep(1)
    
    async def __aenter__(self):
        self._running = True
        self._control_task = asyncio.create_task(self._control_loop())
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._running = False
        if self._control_task:
            self._control_task.cancel()
            try:
                await self._control_task
            except asyncio.CancelledError:
                pass
    
    async def submit(self, coro_func: Callable, *args, **kwargs) -> Any:
        """Submit async work - waits if limit reached (backpressure)"""
        async with await self.semaphore.acquire():  # Block if concurrency limit reached
            return await coro_func(*args, **kwargs)
    
    def get_stats(self) -> dict:
        return self.semaphore.get_stats()
