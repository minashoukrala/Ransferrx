#!/usr/bin/env python3
"""
Performance Monitor

Performance monitoring utility to track validation times and system performance.
Provides metrics collection, timing, and performance analysis.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Callable
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Collects and manages performance metrics."""
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize performance metrics collector.
        
        Args:
            max_history: Maximum number of historical records to keep
        """
        self.max_history = max_history
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self.start_times: Dict[str, float] = {}
    
    def start_timer(self, operation: str) -> None:
        """
        Start timing an operation.
        
        Args:
            operation: Name of the operation being timed
        """
        self.start_times[operation] = time.time()
    
    def end_timer(self, operation: str) -> float:
        """
        End timing an operation and record the duration.
        
        Args:
            operation: Name of the operation being timed
            
        Returns:
            float: Duration in seconds
        """
        if operation not in self.start_times:
            logger.warning(f"Timer for operation '{operation}' was not started")
            return 0.0
        
        duration = time.time() - self.start_times[operation]
        self.metrics[operation].append(duration)
        del self.start_times[operation]
        
        return duration
    
    def get_metrics(self, operation: str) -> Dict[str, Any]:
        """
        Get performance metrics for an operation.
        
        Args:
            operation: Name of the operation
            
        Returns:
            Dict[str, Any]: Performance metrics
        """
        if operation not in self.metrics or not self.metrics[operation]:
            return {
                "count": 0,
                "avg_duration": 0.0,
                "min_duration": 0.0,
                "max_duration": 0.0,
                "median_duration": 0.0,
                "total_duration": 0.0
            }
        
        durations = list(self.metrics[operation])
        
        return {
            "count": len(durations),
            "avg_duration": statistics.mean(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "median_duration": statistics.median(durations),
            "total_duration": sum(durations)
        }
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get performance metrics for all operations.
        
        Returns:
            Dict[str, Dict[str, Any]]: All performance metrics
        """
        return {operation: self.get_metrics(operation) for operation in self.metrics}
    
    def clear_metrics(self, operation: Optional[str] = None) -> None:
        """
        Clear performance metrics.
        
        Args:
            operation: Specific operation to clear, or None to clear all
        """
        if operation:
            if operation in self.metrics:
                self.metrics[operation].clear()
        else:
            self.metrics.clear()
    
    def log_slow_operations(self, threshold: float = 1.0) -> None:
        """
        Log operations that exceed the performance threshold.
        
        Args:
            threshold: Duration threshold in seconds
        """
        for operation, durations in self.metrics.items():
            if durations:
                latest_duration = durations[-1]
                if latest_duration > threshold:
                    logger.warning(f"Slow operation detected: {operation} took {latest_duration:.3f}s")


# Global metrics instance
performance_metrics = PerformanceMetrics()


def time_operation(operation_name: str):
    """
    Decorator to time function execution.
    
    Args:
        operation_name: Name for the operation being timed
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            performance_metrics.start_timer(operation_name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = performance_metrics.end_timer(operation_name)
                if duration > 1.0:  # Log slow operations
                    logger.info(f"Operation '{operation_name}' completed in {duration:.3f}s")
        
        return wrapper
    return decorator


class ValidationPerformanceTracker:
    """Tracks performance of validation operations."""
    
    def __init__(self):
        """Initialize the validation performance tracker."""
        self.validation_times: Dict[str, List[float]] = defaultdict(list)
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.success_counts: Dict[str, int] = defaultdict(int)
    
    def record_validation_time(self, validator_name: str, duration: float) -> None:
        """
        Record validation time for a specific validator.
        
        Args:
            validator_name: Name of the validator
            duration: Duration in seconds
        """
        self.validation_times[validator_name].append(duration)
        
        # Keep only last 100 measurements
        if len(self.validation_times[validator_name]) > 100:
            self.validation_times[validator_name] = self.validation_times[validator_name][-100:]
    
    def record_validation_result(self, validator_name: str, success: bool) -> None:
        """
        Record validation result (success or failure).
        
        Args:
            validator_name: Name of the validator
            success: Whether validation was successful
        """
        if success:
            self.success_counts[validator_name] += 1
        else:
            self.error_counts[validator_name] += 1
    
    def get_validator_performance(self, validator_name: str) -> Dict[str, Any]:
        """
        Get performance metrics for a specific validator.
        
        Args:
            validator_name: Name of the validator
            
        Returns:
            Dict[str, Any]: Performance metrics
        """
        times = self.validation_times.get(validator_name, [])
        
        if not times:
            return {
                "avg_time": 0.0,
                "min_time": 0.0,
                "max_time": 0.0,
                "total_validations": 0,
                "success_rate": 0.0
            }
        
        total_validations = self.success_counts[validator_name] + self.error_counts[validator_name]
        success_rate = (self.success_counts[validator_name] / total_validations * 100) if total_validations > 0 else 0
        
        return {
            "avg_time": statistics.mean(times),
            "min_time": min(times),
            "max_time": max(times),
            "total_validations": total_validations,
            "success_rate": success_rate
        }
    
    def get_all_validator_performance(self) -> Dict[str, Dict[str, Any]]:
        """
        Get performance metrics for all validators.
        
        Returns:
            Dict[str, Dict[str, Any]]: All validator performance metrics
        """
        all_validators = set(self.validation_times.keys()) | set(self.success_counts.keys()) | set(self.error_counts.keys())
        return {validator: self.get_validator_performance(validator) for validator in all_validators}


# Global validation performance tracker
validation_tracker = ValidationPerformanceTracker()


def track_validation_performance(validator_name: str):
    """
    Decorator to track validation performance.
    
    Args:
        validator_name: Name of the validator being tracked
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                validation_tracker.record_validation_result(validator_name, True)
                return result
            except Exception:
                validation_tracker.record_validation_result(validator_name, False)
                raise
            finally:
                duration = time.time() - start_time
                validation_tracker.record_validation_time(validator_name, duration)
        
        return wrapper
    return decorator


class SystemHealthMonitor:
    """Monitors overall system health and performance."""
    
    def __init__(self):
        """Initialize the system health monitor."""
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0
        self.last_health_check = datetime.now()
    
    def record_request(self, success: bool = True) -> None:
        """
        Record a request for health monitoring.
        
        Args:
            success: Whether the request was successful
        """
        self.request_count += 1
        if not success:
            self.error_count += 1
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get current system health status.
        
        Returns:
            Dict[str, Any]: Health status information
        """
        uptime = datetime.now() - self.start_time
        error_rate = (self.error_count / self.request_count * 100) if self.request_count > 0 else 0
        
        return {
            "status": "healthy" if error_rate < 5.0 else "degraded",
            "uptime_seconds": uptime.total_seconds(),
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "error_rate_percent": error_rate,
            "last_health_check": self.last_health_check.isoformat()
        }
    
    def reset_metrics(self) -> None:
        """Reset all health metrics."""
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0
        self.last_health_check = datetime.now()


# Global system health monitor
system_health = SystemHealthMonitor()


def get_performance_summary() -> Dict[str, Any]:
    """
    Get a comprehensive performance summary.
    
    Returns:
        Dict[str, Any]: Performance summary
    """
    return {
        "system_health": system_health.get_health_status(),
        "operation_metrics": performance_metrics.get_all_metrics(),
        "validation_performance": validation_tracker.get_all_validator_performance(),
        "timestamp": datetime.now().isoformat()
    } 