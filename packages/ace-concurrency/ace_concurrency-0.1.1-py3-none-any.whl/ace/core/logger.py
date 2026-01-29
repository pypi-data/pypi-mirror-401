import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone


class ACELogger:
    # Structured logger for ACE decisions and system state
    
    def __init__(self, name: str = "ace", log_level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.logger.propagate = False  # Prevent duplicate logs
        
        # Add handler only if none exist
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(log_level)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    @staticmethod
    def _timestamp() -> str:
        """Get ISO 8601 UTC timestamp"""
        return datetime.now(timezone.utc).isoformat()
    
    def log_decision(
        self,
        event_type: str,
        current_limit: int,
        new_limit: Optional[int],
        active_tasks: int,
        signals: Dict[str, float],
        decision: str,
        reason: str,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> None:
        log_data = {
            "timestamp": self._timestamp(),
            "event_type": event_type,
            "concurrency": {
                "current_limit": current_limit,
                "new_limit": new_limit if new_limit is not None else current_limit,
                "active_tasks": active_tasks,
                "utilization": round(active_tasks / current_limit * 100, 2) if current_limit > 0 else 0
            },
            "signals": {k: round(v, 2) if isinstance(v, float) else v for k, v in signals.items()},
            "decision": decision,
            "reason": reason
        }
        
        if additional_context:
            log_data["context"] = additional_context
        
        self.logger.info(json.dumps(log_data))
    
    def log_task_event(
        self,
        event_type: str,
        task_id: str,
        current_limit: int,
        active_tasks: int,
        wait_time: Optional[float] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> None:
        log_data = {
            "timestamp": self._timestamp(),
            "event_type": event_type,
            "task_id": task_id,
            "concurrency": {
                "current_limit": current_limit,
                "active_tasks": active_tasks,
                "utilization": round(active_tasks / current_limit * 100, 2) if current_limit > 0 else 0
            }
        }
        
        if wait_time is not None:
            log_data["wait_time_seconds"] = round(wait_time, 3)
        
        if additional_context:
            log_data["context"] = additional_context
        
        self.logger.info(json.dumps(log_data))
    
    def log_error(self, error_type: str, error_message: str, context: Optional[Dict[str, Any]] = None) -> None:
        log_data = {
            "timestamp": self._timestamp(),
            "event_type": "error",
            "error_type": error_type,
            "error_message": error_message
        }
        
        if context:
            log_data["context"] = context
        
        self.logger.error(json.dumps(log_data))
    
    def log_info(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        log_data = {
            "timestamp": self._timestamp(),
            "event_type": "info",
            "message": message
        }
        
        if context:
            log_data["context"] = context
        
        self.logger.info(json.dumps(log_data))
