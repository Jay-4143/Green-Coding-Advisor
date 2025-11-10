import structlog
import logging
import sys
from typing import Any, Dict
from .config import settings

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Configure standard logging
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO if not settings.debug else logging.DEBUG,
)

logger = structlog.get_logger()


class GreenCodingLogger:
    """Custom logger for Green Coding Advisor with structured logging"""
    
    def __init__(self):
        self.logger = logger
    
    def log_user_action(self, user_id: int, action: str, details: Dict[str, Any] = None):
        """Log user actions with context"""
        self.logger.info(
            "user_action",
            user_id=user_id,
            action=action,
            details=details or {}
        )
    
    def log_code_analysis(self, submission_id: int, language: str, metrics: Dict[str, Any]):
        """Log code analysis results"""
        self.logger.info(
            "code_analysis",
            submission_id=submission_id,
            language=language,
            green_score=metrics.get("green_score"),
            energy_wh=metrics.get("energy_consumption_wh"),
            co2_g=metrics.get("co2_emissions_g")
        )
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log errors with context"""
        self.logger.error(
            "error_occurred",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context or {}
        )
    
    def log_api_request(self, method: str, path: str, user_id: int = None, status_code: int = None):
        """Log API requests"""
        self.logger.info(
            "api_request",
            method=method,
            path=path,
            user_id=user_id,
            status_code=status_code
        )
    
    def log_performance(self, operation: str, duration_ms: float, details: Dict[str, Any] = None):
        """Log performance metrics"""
        self.logger.info(
            "performance_metric",
            operation=operation,
            duration_ms=duration_ms,
            details=details or {}
        )


# Global logger instance
green_logger = GreenCodingLogger()
