"""
Experiment Manager - Core A/B testing functionality.
"""

import hashlib
import logging
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from neuralforge.ml.ab_testing.schemas import (
    ExperimentCreate,
    ExperimentUpdate,
    ExperimentInfo,
    AssignmentResponse,
    MetricRecord,
    ExperimentResults,
    VariantMetrics,
)
from neuralforge.ml.ab_testing.exceptions import (
    ExperimentNotFoundError,
    ExperimentAlreadyExistsError,
    ExperimentNotRunningError,
    VariantNotFoundError,
)
from neuralforge.ml.ab_testing.assignment import get_assignment_strategy
from neuralforge.ml.ab_testing.statistics import StatisticalAnalyzer
from neuralforge.db.models.ab_experiment import ABExperiment
from neuralforge.db.models.ab_variant import ABVariant
from neuralforge.db.models.ab_assignment import ABAssignment
from neuralforge.db.models.ab_metric import ABMetric

logger = logging.getLogger(__name__)


class ExperimentManager:
    """
    Manage A/B testing experiments.
    
    Provides:
    - Experiment CRUD operations
    - Variant assignment
    - Metrics collection
    - Statistical analysis
    - Winner determination
    
    Example:
        ```python
        manager = ExperimentManager(db_session)
        
        # Create experiment
        experiment = await manager.create_experiment(
            ExperimentCreate(
                name="model-v2-test",
                variants=[...],
                primary_metric="accuracy"
            )
        )
        
        # Get assignment
        assignment = await manager.get_assignment("model-v2-test", "user123")
        
        # Record metric
        await manager.record_metric(
            MetricRecord(
                experiment_name="model-v2-test",
                variant_name="variant_a",
                metric_name="accuracy",
                metric_value=0.95
            )
        )
        
        # Analyze results
        results = await manager.analyze_results(experiment.id)
        ```
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize experiment manager.
        
        Args:
            db: Async database session
        """
        self.db = db
        self.analyzer = StatisticalAnalyzer()

    # ========================================================================
    # Experiment CRUD
    # ========================================================================

    async def create_experiment(
        self,
        experiment_data: ExperimentCreate
    ) -> ExperimentInfo:
        """
        Create a new experiment.
        
        Args:
            experiment_data: Experiment configuration
        
        Returns:
            Created experiment info
        
        Raises:
            ExperimentAlreadyExistsError: If experiment name already exists
        """
        # Check if experiment exists
        existing = await self._get_experiment_by_name(experiment_data.name)
        if existing:
            raise ExperimentAlreadyExistsError(
                f"Experiment '{experiment_data.name}' already exists"
            )

        # Create traffic allocation dict
        traffic_allocation = {
            v.name: v.traffic_percentage
            for v in experiment_data.variants
        }

        # Create experiment
        experiment = ABExperiment(
            name=experiment_data.name,
            description=experiment_data.description,
            status="draft",
            traffic_allocation=traffic_allocation,
            assignment_strategy=experiment_data.assignment_strategy.value,
            primary_metric=experiment_data.primary_metric,
            minimum_sample_size=experiment_data.minimum_sample_size,
            confidence_level=experiment_data.confidence_level,
            minimum_improvement=experiment_data.minimum_improvement,
            duration_days=experiment_data.duration_days,
            created_by=experiment_data.created_by,
        )

        self.db.add(experiment)
        await self.db.flush()  # Get experiment ID

        # Create variants
        for variant_config in experiment_data.variants:
            variant = ABVariant(
                experiment_id=experiment.id,
                name=variant_config.name,
                model_name=variant_config.model_name,
                model_version=variant_config.model_version,
                traffic_percentage=variant_config.traffic_percentage,
                is_control=variant_config.is_control,
                description=variant_config.description,
                config=variant_config.config,
            )
            self.db.add(variant)

        await self.db.commit()
        await self.db.refresh(experiment)

        logger.info(f"Created experiment: {experiment.name} (id={experiment.id})")

        return ExperimentInfo.model_validate(experiment)

    async def get_experiment(self, experiment_id: int) -> ExperimentInfo:
        """
        Get experiment by ID.
        
        Args:
            experiment_id: Experiment ID
        
        Returns:
            Experiment info
        
        Raises:
            ExperimentNotFoundError: If experiment not found
        """
        experiment = await self._get_experiment_by_id(experiment_id)
        if not experiment:
            raise ExperimentNotFoundError(f"Experiment {experiment_id} not found")

        return ExperimentInfo.model_validate(experiment)

    async def list_experiments(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[ExperimentInfo]:
        """
        List experiments.
        
        Args:
            status: Filter by status
            limit: Maximum results
            offset: Results offset
        
        Returns:
            List of experiments
        """
        query = select(ABExperiment)

        if status:
            query = query.where(ABExperiment.status == status)

        query = query.order_by(ABExperiment.created_at.desc())
        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        experiments = result.scalars().all()

        return [ExperimentInfo.model_validate(exp) for exp in experiments]

    async def update_experiment(
        self,
        experiment_id: int,
        updates: ExperimentUpdate
    ) -> ExperimentInfo:
        """
        Update experiment.
        
        Args:
            experiment_id: Experiment ID
            updates: Fields to update
        
        Returns:
            Updated experiment info
        
        Raises:
            ExperimentNotFoundError: If experiment not found
        """
        experiment = await self._get_experiment_by_id(experiment_id)
        if not experiment:
            raise ExperimentNotFoundError(f"Experiment {experiment_id} not found")

        # Update fields
        update_data = updates.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(experiment, key, value)

        experiment.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(experiment)

        logger.info(f"Updated experiment: {experiment.name} (id={experiment.id})")

        return ExperimentInfo.model_validate(experiment)

    async def delete_experiment(self, experiment_id: int) -> bool:
        """
        Delete experiment.
        
        Args:
            experiment_id: Experiment ID
        
        Returns:
            True if deleted
        """
        experiment = await self._get_experiment_by_id(experiment_id)
        if not experiment:
            return False

        await self.db.delete(experiment)
        await self.db.commit()

        logger.info(f"Deleted experiment: {experiment.name} (id={experiment.id})")

        return True

    # ========================================================================
    # Experiment Control
    # ========================================================================

    async def start_experiment(self, experiment_id: int) -> ExperimentInfo:
        """Start experiment."""
        experiment = await self._get_experiment_by_id(experiment_id)
        if not experiment:
            raise ExperimentNotFoundError(f"Experiment {experiment_id} not found")

        experiment.status = "running"
        experiment.start_time = datetime.utcnow()

        if experiment.duration_days:
            experiment.end_time = experiment.start_time + timedelta(days=experiment.duration_days)

        await self.db.commit()
        await self.db.refresh(experiment)

        logger.info(f"Started experiment: {experiment.name}")

        return ExperimentInfo.model_validate(experiment)

    async def stop_experiment(self, experiment_id: int) -> ExperimentInfo:
        """Stop experiment."""
        experiment = await self._get_experiment_by_id(experiment_id)
        if not experiment:
            raise ExperimentNotFoundError(f"Experiment {experiment_id} not found")

        experiment.status = "completed"
        experiment.end_time = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(experiment)

        logger.info(f"Stopped experiment: {experiment.name}")

        return ExperimentInfo.model_validate(experiment)

    # ========================================================================
    # Assignment
    # ========================================================================

    async def get_assignment(
        self,
        experiment_name: str,
        user_id: str
    ) -> AssignmentResponse:
        """
        Get variant assignment for user.
        
        Args:
            experiment_name: Experiment name
            user_id: User identifier
        
        Returns:
            Assignment response
        
        Raises:
            ExperimentNotFoundError: If experiment not found
            ExperimentNotRunningError: If experiment not running
        """
        # Get experiment
        experiment = await self._get_experiment_by_name(experiment_name)
        if not experiment:
            raise ExperimentNotFoundError(f"Experiment '{experiment_name}' not found")

        if experiment.status != "running":
            raise ExperimentNotRunningError(
                f"Experiment '{experiment_name}' is not running (status: {experiment.status})"
            )

        # Check for existing assignment
        existing = await self._get_existing_assignment(experiment.id, user_id)
        if existing:
            variant = await self._get_variant_by_id(existing.variant_id)
            return self._create_assignment_response(experiment, variant, existing.assigned_at)

        # Get active variants
        variants = await self._get_active_variants(experiment.id)
        if not variants:
            raise VariantNotFoundError(f"No active variants for experiment '{experiment_name}'")

        # Assign variant
        strategy = get_assignment_strategy(experiment.assignment_strategy)
        assigned_variant = strategy.assign(user_id, variants)

        # Create assignment record
        user_hash = hashlib.md5(user_id.encode()).hexdigest()
        assignment = ABAssignment(
            experiment_id=experiment.id,
            variant_id=assigned_variant.id,
            user_id=user_id,
            user_hash=user_hash,
        )

        self.db.add(assignment)
        await self.db.commit()

        logger.debug(f"Assigned user {user_id} to variant {assigned_variant.name}")

        return self._create_assignment_response(experiment, assigned_variant, assignment.assigned_at)

    # ========================================================================
    # Metrics
    # ========================================================================

    async def record_metric(self, metric_data: MetricRecord):
        """
        Record metric for variant.
        
        Args:
            metric_data: Metric data
        """
        # Get experiment and variant
        experiment = await self._get_experiment_by_name(metric_data.experiment_name)
        if not experiment:
            raise ExperimentNotFoundError(f"Experiment '{metric_data.experiment_name}' not found")

        variant = await self._get_variant_by_name(experiment.id, metric_data.variant_name)
        if not variant:
            raise VariantNotFoundError(
                f"Variant '{metric_data.variant_name}' not found in experiment '{metric_data.experiment_name}'"
            )

        # Create metric record
        metric = ABMetric(
            experiment_id=experiment.id,
            variant_id=variant.id,
            metric_name=metric_data.metric_name,
            metric_value=metric_data.metric_value,
            metric_type=metric_data.metric_type,
            user_id=metric_data.user_id,
            prediction_id=metric_data.prediction_id,
        )

        self.db.add(metric)
        await self.db.commit()

    # ========================================================================
    # Analysis
    # ========================================================================

    async def analyze_results(self, experiment_id: int) -> ExperimentResults:
        """
        Analyze experiment results.
        
        Args:
            experiment_id: Experiment ID
        
        Returns:
            Experiment results with statistical analysis
        """
        experiment = await self._get_experiment_by_id(experiment_id)
        if not experiment:
            raise ExperimentNotFoundError(f"Experiment {experiment_id} not found")

        # Get variants
        variants = await self._get_active_variants(experiment.id)
        control_variant = next((v for v in variants if v.is_control), None)

        # Get metrics for each variant
        variant_metrics_list = []
        control_values = []

        for variant in variants:
            values = await self._get_variant_metrics(experiment.id, variant.id, experiment.primary_metric)

            if variant.is_control:
                control_values = values

            if values:
                mean, std_dev = self.analyzer.calculate_mean_std(values)
                ci = self.analyzer.calculate_confidence_interval(values, experiment.confidence_level)

                variant_metrics_list.append(VariantMetrics(
                    variant_name=variant.name,
                    sample_size=len(values),
                    mean=mean,
                    std_dev=std_dev,
                    confidence_interval=ci
                ))

        # Determine winner
        winner = None
        winner_confidence = None
        p_value = None
        is_significant = False

        if control_variant and len(variants) == 2:
            # Simple A/B test
            test_variant = next((v for v in variants if not v.is_control), None)
            if test_variant:
                test_values = await self._get_variant_metrics(
                    experiment.id, test_variant.id, experiment.primary_metric
                )

                winner_name, confidence, is_sig = self.analyzer.determine_winner(
                    control_values,
                    test_values,
                    experiment.confidence_level,
                    experiment.minimum_improvement
                )

                if winner_name == "variant":
                    winner = test_variant.name
                elif winner_name == "control":
                    winner = control_variant.name

                winner_confidence = confidence
                is_significant = is_sig

                _, p_value = self.analyzer.calculate_t_test(control_values, test_values)

        # Check sample size
        has_sufficient_sample = all(
            vm.sample_size >= experiment.minimum_sample_size
            for vm in variant_metrics_list
        )

        # Generate recommendation
        if not has_sufficient_sample:
            recommendation = f"Continue experiment - need {experiment.minimum_sample_size} samples per variant"
        elif not is_significant:
            recommendation = "No significant difference detected - consider running longer"
        elif winner:
            recommendation = f"Rollout {winner} to 100%"
        else:
            recommendation = "Inconclusive - review results manually"

        return ExperimentResults(
            experiment_id=experiment.id,
            experiment_name=experiment.name,
            status=experiment.status,
            primary_metric=experiment.primary_metric,
            variants=variant_metrics_list,
            winner=winner,
            winner_confidence=winner_confidence,
            p_value=p_value,
            is_significant=is_significant,
            has_sufficient_sample=has_sufficient_sample,
            recommendation=recommendation
        )

    # ========================================================================
    # Helper Methods
    # ========================================================================

    async def _get_experiment_by_id(self, experiment_id: int) -> Optional[ABExperiment]:
        """Get experiment by ID."""
        result = await self.db.execute(
            select(ABExperiment).where(ABExperiment.id == experiment_id)
        )
        return result.scalar_one_or_none()

    async def _get_experiment_by_name(self, name: str) -> Optional[ABExperiment]:
        """Get experiment by name."""
        result = await self.db.execute(
            select(ABExperiment).where(ABExperiment.name == name)
        )
        return result.scalar_one_or_none()

    async def _get_variant_by_id(self, variant_id: int) -> Optional[ABVariant]:
        """Get variant by ID."""
        result = await self.db.execute(
            select(ABVariant).where(ABVariant.id == variant_id)
        )
        return result.scalar_one_or_none()

    async def _get_variant_by_name(self, experiment_id: int, name: str) -> Optional[ABVariant]:
        """Get variant by name."""
        result = await self.db.execute(
            select(ABVariant).where(
                and_(
                    ABVariant.experiment_id == experiment_id,
                    ABVariant.name == name
                )
            )
        )
        return result.scalar_one_or_none()

    async def _get_active_variants(self, experiment_id: int) -> List[ABVariant]:
        """Get active variants for experiment."""
        result = await self.db.execute(
            select(ABVariant).where(
                and_(
                    ABVariant.experiment_id == experiment_id,
                    ABVariant.is_active.is_(True)
                )
            ).order_by(ABVariant.id)
        )
        return list(result.scalars().all())

    async def _get_existing_assignment(
        self,
        experiment_id: int,
        user_id: str
    ) -> Optional[ABAssignment]:
        """Get existing assignment for user."""
        result = await self.db.execute(
            select(ABAssignment).where(
                and_(
                    ABAssignment.experiment_id == experiment_id,
                    ABAssignment.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()

    async def _get_variant_metrics(
        self,
        experiment_id: int,
        variant_id: int,
        metric_name: str
    ) -> List[float]:
        """Get metric values for variant."""
        result = await self.db.execute(
            select(ABMetric.metric_value).where(
                and_(
                    ABMetric.experiment_id == experiment_id,
                    ABMetric.variant_id == variant_id,
                    ABMetric.metric_name == metric_name
                )
            )
        )
        return [float(v) for v in result.scalars().all()]

    def _create_assignment_response(
        self,
        experiment: ABExperiment,
        variant: ABVariant,
        assigned_at: datetime
    ) -> AssignmentResponse:
        """Create assignment response."""
        return AssignmentResponse(
            experiment_name=experiment.name,
            variant_name=variant.name,
            model_name=variant.model_name,
            model_version=variant.model_version,
            is_control=variant.is_control,
            assigned_at=assigned_at
        )
