"""Health Checker - Health check endpoints."""
import logging
logger = logging.getLogger(__name__)

class HealthChecker:
    """Manages health checks."""
    def __init__(self, app):
        self.app = app
        self.checks = {}
        logger.info("Initialized HealthChecker")

    def add_check(self, name: str, check_fn):
        """Add health check."""
        self.checks[name] = check_fn

    async def run_checks(self) -> dict:
        """Run all health checks."""
        results = {}
        for name, check_fn in self.checks.items():
            try:
                results[name] = await check_fn()
            except Exception as e:
                results[name] = {"status": "unhealthy", "error": str(e)}
        return results
