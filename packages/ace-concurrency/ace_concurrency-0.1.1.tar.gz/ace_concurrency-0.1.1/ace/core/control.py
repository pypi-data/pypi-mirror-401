import time
import threading
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from ace.core.signals import SystemSignals
from ace.core.logger import ACELogger


class Decision(Enum):
    INCREASE = "increase"
    DECREASE = "decrease"
    NO_CHANGE = "no_change"


@dataclass
class AIMDConfig:
    """AIMD algorithm configuration"""
    min_limit: int = 5
    max_limit: int = 200
    initial_limit: int = 20
    increase_step: int = 2
    decrease_factor: float = 0.5
    cpu_threshold: float = 80.0          
    memory_threshold: float = 85.0       
    cpu_increase_threshold: float = 40.0 
    memory_increase_threshold: float = 50.0 
    queue_threshold: int = 100
    event_loop_lag_threshold_ms: float = 50.0
    cooldown_seconds: float = 5.0
    adjustment_interval_seconds: float = 2.0
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if not (0 < self.min_limit < self.max_limit):
            raise ValueError(f"min_limit ({self.min_limit}) must be > 0 and < max_limit ({self.max_limit})")
        if not (self.min_limit <= self.initial_limit <= self.max_limit):
            raise ValueError(f"initial_limit ({self.initial_limit}) must be between min_limit and max_limit")
        if not (0 < self.increase_step < self.max_limit):
            raise ValueError(f"increase_step ({self.increase_step}) must be > 0")
        if not (0 < self.decrease_factor < 1):
            raise ValueError(f"decrease_factor ({self.decrease_factor}) must be between 0 and 1")
        if not (0 <= self.cpu_threshold <= 100):
            raise ValueError(f"cpu_threshold ({self.cpu_threshold}) must be 0-100")
        if not (0 <= self.memory_threshold <= 100):
            raise ValueError(f"memory_threshold ({self.memory_threshold}) must be 0-100")
        if self.cpu_increase_threshold >= self.cpu_threshold:
            raise ValueError(f"cpu_increase_threshold ({self.cpu_increase_threshold}) must be < cpu_threshold ({self.cpu_threshold})")
        if self.memory_increase_threshold >= self.memory_threshold:
            raise ValueError(f"memory_increase_threshold ({self.memory_increase_threshold}) must be < memory_threshold ({self.memory_threshold})")
        if self.cooldown_seconds < 0 or self.adjustment_interval_seconds < 0:
            raise ValueError("cooldown_seconds and adjustment_interval_seconds must be >= 0")


class ACEController:
    
    def __init__(self, config: AIMDConfig, logger: Optional[ACELogger] = None):
        self.config = config
        self.logger = logger or ACELogger()
        self._last_adjustment_time = 0.0
        self._last_decision = Decision.NO_CHANGE.value
        self._lock = threading.Lock() 
    
    def should_adjust(self) -> bool:
        # Check if cooldown period has elapsed
        return (time.time() - self._last_adjustment_time) >= self.config.cooldown_seconds
    
    def _is_system_stressed(self, signals: SystemSignals) -> tuple[bool, str]:
        # Check if any signal exceeds threshold
        if signals.cpu_percent > self.config.cpu_threshold:
            return True, f"CPU usage {signals.cpu_percent:.1f}% > {self.config.cpu_threshold}%"
        
        if signals.memory_percent > self.config.memory_threshold:
            return True, f"Memory usage {signals.memory_percent:.1f}% > {self.config.memory_threshold}%"
        
        if signals.queue_depth > self.config.queue_threshold:
            return True, f"Queue depth {signals.queue_depth} > {self.config.queue_threshold}"
        
        if signals.event_loop_lag_ms > self.config.event_loop_lag_threshold_ms:
            return True, f"Event loop lag {signals.event_loop_lag_ms:.1f}ms > {self.config.event_loop_lag_threshold_ms}ms"
        
        return False, "All signals within healthy thresholds"
    
    def adjust_limit(self, current_limit: int, active_tasks: int, signals: SystemSignals) -> int:
        with self._lock:  # Thread-safe adjustment
            # Apply AIMD
            if not self.should_adjust():
                return current_limit
            
            is_stressed, stress_reason = self._is_system_stressed(signals)
            utilization = active_tasks / current_limit if current_limit > 0 else 0
            
            new_limit = current_limit
            decision = Decision.NO_CHANGE
            reason = "Within cooldown period or no clear signal"
            
            if is_stressed:
                # Multiplicative decrease
                new_limit = max(self.config.min_limit, int(current_limit * self.config.decrease_factor))
                decision = Decision.DECREASE
                reason = f"System stressed: {stress_reason}"
                self._last_adjustment_time = time.time()
            
            elif signals.cpu_percent < self.config.cpu_increase_threshold and signals.memory_percent < self.config.memory_increase_threshold:
                # Proactive increase when resources are very available
                new_limit = min(self.config.max_limit, current_limit + self.config.increase_step)
                decision = Decision.INCREASE
                reason = f"Resources available: CPU {signals.cpu_percent:.1f}% < {self.config.cpu_increase_threshold}%, Memory {signals.memory_percent:.1f}% < {self.config.memory_increase_threshold}%"
                self._last_adjustment_time = time.time()
                
            elif utilization > 0.8:
                # Reactive increase when highly utilized
                new_limit = min(self.config.max_limit, current_limit + self.config.increase_step)
                decision = Decision.INCREASE
                reason = f"High utilization ({utilization*100:.1f}%) and system healthy"
                self._last_adjustment_time = time.time()
            
            else:
                reason = f"Utilization moderate ({utilization*100:.1f}%), system healthy, no adjustment needed"
            
            if decision != Decision.NO_CHANGE or self._last_decision != decision.value:
                self.logger.log_decision(
                    event_type="limit_adjustment",
                    current_limit=current_limit,
                    new_limit=new_limit,
                    active_tasks=active_tasks,
                    signals=signals.to_dict(),
                    decision=decision.value,
                    reason=reason,
                    additional_context={
                        "utilization_percent": round(utilization * 100, 2),
                        "aimd_state": decision.value
                    }
                )
                self._last_decision = decision.value
            
            return new_limit
    
    def get_initial_limit(self) -> int:
        return self.config.initial_limit
