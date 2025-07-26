#!/usr/bin/env python3
"""
Error Handler

Centralized error handling for consistent error responses across the application.
Provides standardized error codes, messages, and logging.
"""

import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationError(HTTPException):
    """Custom validation error with standardized format."""
    
    def __init__(self, reason_code: str, message: str, status_code: int = 400):
        self.reason_code = reason_code
        self.message = message
        self.status_code = status_code
        super().__init__(status_code=status_code, detail=self._format_detail())
    
    def _format_detail(self) -> Dict[str, Any]:
        """Format error detail with timestamp and structured data."""
        return {
            "reason_code": self.reason_code,
            "message": self.message,
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": "validation_error"
        }


class BusinessRuleError(HTTPException):
    """Custom business rule error for regulatory violations."""
    
    def __init__(self, reason_code: str, message: str, status_code: int = 403):
        self.reason_code = reason_code
        self.message = message
        self.status_code = status_code
        super().__init__(status_code=status_code, detail=self._format_detail())
    
    def _format_detail(self) -> Dict[str, Any]:
        """Format error detail with timestamp and structured data."""
        return {
            "reason_code": self.reason_code,
            "message": self.message,
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": "business_rule_error"
        }


class SystemError(HTTPException):
    """Custom system error for internal failures."""
    
    def __init__(self, reason_code: str, message: str, status_code: int = 500):
        self.reason_code = reason_code
        self.message = message
        self.status_code = status_code
        super().__init__(status_code=status_code, detail=self._format_detail())
    
    def _format_detail(self) -> Dict[str, Any]:
        """Format error detail with timestamp and structured data."""
        return {
            "reason_code": self.reason_code,
            "message": self.message,
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": "system_error"
        }


def log_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """
    Log error with context for debugging and monitoring.
    
    Args:
        error: The exception that occurred
        context: Additional context information
    """
    error_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if context:
        error_data.update(context)
    
    if isinstance(error, (ValidationError, BusinessRuleError, SystemError)):
        logger.warning(f"Application error: {error_data}")
    else:
        logger.error(f"Unexpected error: {error_data}")


def handle_validation_error(reason_code: str, message: str, context: Optional[Dict[str, Any]] = None) -> ValidationError:
    """
    Create and log a validation error.
    
    Args:
        reason_code: NCPDP reason code
        message: Human-readable error message
        context: Additional context for logging
        
    Returns:
        ValidationError: Formatted validation error
    """
    error = ValidationError(reason_code, message)
    log_error(error, context)
    return error


def handle_business_rule_error(reason_code: str, message: str, context: Optional[Dict[str, Any]] = None) -> BusinessRuleError:
    """
    Create and log a business rule error.
    
    Args:
        reason_code: NCPDP reason code
        message: Human-readable error message
        context: Additional context for logging
        
    Returns:
        BusinessRuleError: Formatted business rule error
    """
    error = BusinessRuleError(reason_code, message)
    log_error(error, context)
    return error


def handle_system_error(reason_code: str, message: str, context: Optional[Dict[str, Any]] = None) -> SystemError:
    """
    Create and log a system error.
    
    Args:
        reason_code: NCPDP reason code
        message: Human-readable error message
        context: Additional context for logging
        
    Returns:
        SystemError: Formatted system error
    """
    error = SystemError(reason_code, message)
    log_error(error, context)
    return error


# Standard error codes and messages
ERROR_CODES = {
    # Validation Errors (400)
    "BY": "Invalid data format or missing required fields",
    "BC": "Missing digital signature for controlled substance",
    "BD": "Invalid quantity qualifiers",
    "BE": "Invalid refills consistency",
    "BF": "Invalid prescription expiration",
    "BG": "Invalid pharmacy identification",
    "BH": "Duplicate transfer detected",
    
    # Business Rule Errors (403)
    "CW": "Prescription expired (older than 1 year)",
    "CX": "Controlled substance transfer not allowed",
    "CY": "Transfer limit exceeded",
    
    # System Errors (500)
    "SY": "System error - unable to process request",
    "SZ": "Database connection error",
    "SA": "Certificate validation error",
    "SB": "XML parsing error",
    "SC": "Schema validation error"
}


def get_error_message(reason_code: str) -> str:
    """
    Get standardized error message for a reason code.
    
    Args:
        reason_code: NCPDP reason code
        
    Returns:
        str: Standardized error message
    """
    return ERROR_CODES.get(reason_code, "Unknown error")


def create_error_response(reason_code: str, custom_message: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        reason_code: NCPDP reason code
        custom_message: Optional custom message (overrides standard message)
        context: Additional context for logging
        
    Returns:
        Dict[str, Any]: Standardized error response
    """
    message = custom_message or get_error_message(reason_code)
    
    # Determine status code based on reason code
    if reason_code.startswith(('BY', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH')):
        status_code = 400
    elif reason_code.startswith(('CW', 'CX', 'CY')):
        status_code = 403
    else:
        status_code = 500
    
    error_response = {
        "status": "error",
        "reason_code": reason_code,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Log the error
    log_error(Exception(message), {"reason_code": reason_code, "context": context})
    
    return error_response 