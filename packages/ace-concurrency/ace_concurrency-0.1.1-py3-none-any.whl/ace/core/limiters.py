import asyncio
import uuid
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore, Lock
from typing import Optional, Callable, Any
from contextlib import asynccontextmanager
from ace.core.logger import ACELogger


class ACESemaphore:
    # Adaptive async semaphore with dynamic limit adjustment
    
    def __init__(self, initial_limit: int, logger: Optional[ACELogger] = None):
        self._limit = initial_limit
        self._active = 0
        self._semaphore = asyncio.Semaphore(initial_limit)  # Use stdlib Semaphore for reliability
        self._lock = asyncio.Lock()
        self.logger = logger or ACELogger()
    
    async def acquire(self):
        """Acquire slot - blocks if limit reached (backpressure)"""
        task_id = str(uuid.uuid4())[:8]
        wait_start = time.time()
        
        await self._semaphore.acquire()  # Standard asyncio semaphore
        
        async with self._lock:
            self._active += 1
        
        wait_time = time.time() - wait_start
        if wait_time > 0.001:
            self.logger.log_task_event(
                event_type="task_acquired_after_wait",
                task_id=task_id,
                current_limit=self._limit,
                active_tasks=self._active,
                wait_time=wait_time
            )
        
        return self  # Return context manager that releases
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        async with self._lock:
            self._active = max(0, self._active - 1)  # Safety: never negative
        self._semaphore.release()
    
    async def set_limit(self, new_limit: int) -> None:
        """Dynamically adjust concurrency limit"""
        new_limit = max(1, min(new_limit, 10000))  # Sanity bounds: 1-10000
        
        async with self._lock:
            diff = new_limit - self._limit
            self._limit = new_limit
            
            if diff < 0:  # Decrease: acquire extra permits
                for _ in range(abs(diff)):
                    await self._semaphore.acquire()
            elif diff > 0:  # Increase: release permits
                for _ in range(diff):
                    self._semaphore.release()
    
    def get_stats(self) -> dict:
        """Return current stats (active, limit, waiting)"""
        return {
            "limit": self._limit,
            "active": self._active,
            "waiting": self._semaphore._value < 0 and abs(self._semaphore._value) or 0
        }


class ACEThreadPoolLimiter:
    # Thread pool with dynamic concurrency control and backpressure
    
    def __init__(self, initial_limit: int, logger: Optional[ACELogger] = None):
        self._limit = initial_limit
        self._executor = ThreadPoolExecutor(max_workers=initial_limit)
        self._semaphore = Semaphore(initial_limit)
        self._lock = Lock()
        self._active_tasks = 0
        self._queue_depth = 0
        self.logger = logger or ACELogger()
    
    def submit(self, fn: Callable, *args, **kwargs) -> Any:
        self._semaphore.acquire()  # Backpressure point
        
        with self._lock:
            self._active_tasks += 1
            self._queue_depth = self._executor._work_queue.qsize()
        
        def wrapper():
            try:
                return fn(*args, **kwargs)
            finally:
                with self._lock:
                    self._active_tasks -= 1
                self._semaphore.release()
        
        return self._executor.submit(wrapper)
    
    def set_limit(self, new_limit: int):
        with self._lock:
            diff = new_limit - self._limit
            self._limit = new_limit
            
            if diff > 0:
                for _ in range(diff):
                    self._semaphore.release()
            elif diff < 0:
                for _ in range(abs(diff)):
                    self._semaphore.acquire()
    
    def get_stats(self) -> dict:
        with self._lock:
            return {
                "limit": self._limit,
                "active": self._active_tasks,
                "queue_depth": self._queue_depth
            }
    
    def shutdown(self, wait: bool = True):
        self._executor.shutdown(wait=wait)
