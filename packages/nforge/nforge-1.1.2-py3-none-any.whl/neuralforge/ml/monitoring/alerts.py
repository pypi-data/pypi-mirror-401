"""
Alert Manager - Manage alerts and notifications.
"""

import logging
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from neuralforge.ml.monitoring.schemas import AlertRuleCreate, AlertRuleInfo, AlertInfo
from neuralforge.ml.monitoring.exceptions import AlertRuleNotFoundError, AlertNotFoundError
from neuralforge.ml.monitoring.metrics import MetricsCollector
from neuralforge.db.models.alert_rule import AlertRule
from neuralforge.db.models.prediction_alert import PredictionAlert

logger = logging.getLogger(__name__)


class AlertManager:
    """
    Manage alerts and notifications.
    
    Example:
        ```python
        manager = AlertManager(db_session)
        
        # Create alert rule
        rule = await manager.create_rule(
            AlertRuleCreate(
                name="high-latency",
                metric_name="p95_latency",
                operator="gt",
                threshold=100.0,
                severity="warning"
            )
        )
        
        # Check thresholds
        await manager.check_all_rules()
        ```
    """

    def __init__(self, db: AsyncSession):
        """Initialize alert manager."""
        self.db = db
        self.metrics = MetricsCollector(db)

    # ========================================================================
    # Alert Rules
    # ========================================================================

    async def create_rule(
        self,
        rule_data: AlertRuleCreate
    ) -> AlertRuleInfo:
        """Create alert rule."""
        rule = AlertRule(
            name=rule_data.name,
            description=rule_data.description,
            model_name=rule_data.model_name,
            model_version=rule_data.model_version,
            metric_name=rule_data.metric_name,
            operator=rule_data.operator,
            threshold=rule_data.threshold,
            window_minutes=rule_data.window_minutes,
            severity=rule_data.severity.value,
            channels=rule_data.channels,
        )

        self.db.add(rule)
        await self.db.commit()
        await self.db.refresh(rule)

        logger.info(f"Created alert rule: {rule.name}")

        return AlertRuleInfo.model_validate(rule)

    async def get_rule(self, rule_id: int) -> AlertRuleInfo:
        """Get alert rule by ID."""
        result = await self.db.execute(
            select(AlertRule).where(AlertRule.id == rule_id)
        )
        rule = result.scalar_one_or_none()

        if not rule:
            raise AlertRuleNotFoundError(f"Alert rule {rule_id} not found")

        return AlertRuleInfo.model_validate(rule)

    async def list_rules(
        self,
        is_active: Optional[bool] = None
    ) -> List[AlertRuleInfo]:
        """List alert rules."""
        query = select(AlertRule)

        if is_active is not None:
            query = query.where(AlertRule.is_active == is_active)

        result = await self.db.execute(query)
        rules = result.scalars().all()

        return [AlertRuleInfo.model_validate(r) for r in rules]

    async def delete_rule(self, rule_id: int) -> bool:
        """Delete alert rule."""
        result = await self.db.execute(
            select(AlertRule).where(AlertRule.id == rule_id)
        )
        rule = result.scalar_one_or_none()

        if not rule:
            return False

        await self.db.delete(rule)
        await self.db.commit()

        logger.info(f"Deleted alert rule: {rule.name}")

        return True

    # ========================================================================
    # Alerts
    # ========================================================================

    async def trigger_alert(
        self,
        alert_type: str,
        message: str,
        severity: str,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        threshold_value: Optional[float] = None,
        actual_value: Optional[float] = None,
        **metadata
    ) -> AlertInfo:
        """Trigger an alert."""
        alert = PredictionAlert(
            alert_type=alert_type,
            severity=severity,
            model_name=model_name,
            model_version=model_version,
            message=message,
            threshold_value=threshold_value,
            actual_value=actual_value,
            metadata=metadata if metadata else None,
        )

        self.db.add(alert)
        await self.db.commit()
        await self.db.refresh(alert)

        logger.warning(f"Alert triggered: {alert_type} - {message}")

        return AlertInfo.model_validate(alert)

    async def get_alert(self, alert_id: int) -> AlertInfo:
        """Get alert by ID."""
        result = await self.db.execute(
            select(PredictionAlert).where(PredictionAlert.id == alert_id)
        )
        alert = result.scalar_one_or_none()

        if not alert:
            raise AlertNotFoundError(f"Alert {alert_id} not found")

        return AlertInfo.model_validate(alert)

    async def list_alerts(
        self,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100
    ) -> List[AlertInfo]:
        """List alerts."""
        query = select(PredictionAlert)

        conditions = []
        if status:
            conditions.append(PredictionAlert.status == status)
        if severity:
            conditions.append(PredictionAlert.severity == severity)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.order_by(PredictionAlert.triggered_at.desc()).limit(limit)

        result = await self.db.execute(query)
        alerts = result.scalars().all()

        return [AlertInfo.model_validate(a) for a in alerts]

    async def acknowledge_alert(self, alert_id: int) -> AlertInfo:
        """Acknowledge an alert."""
        result = await self.db.execute(
            select(PredictionAlert).where(PredictionAlert.id == alert_id)
        )
        alert = result.scalar_one_or_none()

        if not alert:
            raise AlertNotFoundError(f"Alert {alert_id} not found")

        alert.status = "acknowledged"
        alert.acknowledged_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(alert)

        return AlertInfo.model_validate(alert)

    async def resolve_alert(self, alert_id: int) -> AlertInfo:
        """Resolve an alert."""
        result = await self.db.execute(
            select(PredictionAlert).where(PredictionAlert.id == alert_id)
        )
        alert = result.scalar_one_or_none()

        if not alert:
            raise AlertNotFoundError(f"Alert {alert_id} not found")

        alert.status = "resolved"
        alert.resolved_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(alert)

        return AlertInfo.model_validate(alert)

    # ========================================================================
    # Threshold Checking
    # ========================================================================

    async def check_rule(self, rule: AlertRule) -> bool:
        """
        Check if a rule's threshold is exceeded.
        
        Returns:
            True if alert was triggered
        """
        if not rule.is_active:
            return False

        time_range = f"{rule.window_minutes}m"

        try:
            # Get metric value based on metric name
            if "latency" in rule.metric_name:
                stats = await self.metrics.get_latency_stats(
                    rule.model_name,
                    time_range,
                    rule.model_version
                )
                if rule.metric_name == "p95_latency":
                    actual_value = stats.p95
                elif rule.metric_name == "p99_latency":
                    actual_value = stats.p99
                elif rule.metric_name == "avg_latency":
                    actual_value = stats.avg
                else:
                    actual_value = stats.max

            elif rule.metric_name == "error_rate":
                stats = await self.metrics.get_error_stats(
                    rule.model_name,
                    time_range,
                    rule.model_version
                )
                actual_value = stats.error_rate

            elif rule.metric_name == "confidence":
                stats = await self.metrics.get_confidence_distribution(
                    rule.model_name,
                    time_range,
                    rule.model_version
                )
                actual_value = stats.avg_confidence

            else:
                logger.warning(f"Unknown metric: {rule.metric_name}")
                return False

            # Check threshold
            threshold_exceeded = False
            if rule.operator == "gt":
                threshold_exceeded = actual_value > rule.threshold
            elif rule.operator == "lt":
                threshold_exceeded = actual_value < rule.threshold
            elif rule.operator == "eq":
                threshold_exceeded = abs(actual_value - rule.threshold) < 0.01

            if threshold_exceeded:
                await self.trigger_alert(
                    alert_type=rule.metric_name,
                    message=f"{rule.name}: {rule.metric_name} is {actual_value:.2f} (threshold: {rule.threshold})",
                    severity=rule.severity,
                    model_name=rule.model_name,
                    model_version=rule.model_version,
                    threshold_value=rule.threshold,
                    actual_value=actual_value
                )
                return True

        except Exception as e:
            logger.error(f"Error checking rule {rule.name}: {e}")

        return False

    async def check_all_rules(self) -> int:
        """
        Check all active rules.
        
        Returns:
            Number of alerts triggered
        """
        rules = await self.list_rules(is_active=True)

        alerts_triggered = 0
        for rule_info in rules:
            # Get full rule object
            result = await self.db.execute(
                select(AlertRule).where(AlertRule.id == rule_info.id)
            )
            rule = result.scalar_one()

            if await self.check_rule(rule):
                alerts_triggered += 1

        return alerts_triggered
