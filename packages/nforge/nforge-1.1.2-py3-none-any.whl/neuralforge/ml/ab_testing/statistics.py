"""
Statistical analysis for A/B testing.
"""

import math
from typing import List, Tuple, Optional
from scipy import stats
import numpy as np


class StatisticalAnalyzer:
    """Perform statistical analysis on experiment results."""

    def calculate_t_test(
        self,
        control_values: List[float],
        variant_values: List[float]
    ) -> Tuple[float, float]:
        """
        Perform independent t-test.
        
        Args:
            control_values: Control group values
            variant_values: Variant group values
        
        Returns:
            Tuple of (t_statistic, p_value)
        """
        if len(control_values) < 2 or len(variant_values) < 2:
            return 0.0, 1.0

        t_stat, p_value = stats.ttest_ind(control_values, variant_values)
        return float(t_stat), float(p_value)

    def calculate_chi_square(
        self,
        control_counts: List[int],
        variant_counts: List[int]
    ) -> Tuple[float, float]:
        """
        Perform chi-square test for categorical data.
        
        Args:
            control_counts: Control group category counts
            variant_counts: Variant group category counts
        
        Returns:
            Tuple of (chi2_statistic, p_value)
        
        Example:
            # For binary outcomes (success/failure)
            control_counts = [800, 200]  # 800 success, 200 failure
            variant_counts = [850, 150]  # 850 success, 150 failure
            chi2, p_value = analyzer.calculate_chi_square(control_counts, variant_counts)
        """
        if len(control_counts) < 2 or len(variant_counts) < 2:
            return 0.0, 1.0

        # Create contingency table
        contingency_table = np.array([control_counts, variant_counts])

        # Perform chi-square test
        chi2_stat, p_value, _dof, _expected = stats.chi2_contingency(contingency_table)

        return float(chi2_stat), float(p_value)

    def calculate_confidence_interval(
        self,
        values: List[float],
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Calculate confidence interval.
        
        Args:
            values: Sample values
            confidence: Confidence level (default: 0.95)
        
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        if len(values) < 2:
            mean = values[0] if values else 0.0
            return (mean, mean)

        mean = np.mean(values)
        std_err = stats.sem(values)
        margin = std_err * stats.t.ppf((1 + confidence) / 2, len(values) - 1)

        return (float(mean - margin), float(mean + margin))

    def calculate_mean_std(
        self,
        values: List[float]
    ) -> Tuple[float, float]:
        """
        Calculate mean and standard deviation.
        
        Args:
            values: Sample values
        
        Returns:
            Tuple of (mean, std_dev)
        """
        if not values:
            return 0.0, 0.0

        return float(np.mean(values)), float(np.std(values, ddof=1))

    def has_sufficient_sample_size(
        self,
        control_size: int,
        variant_size: int,
        minimum: int = 1000
    ) -> bool:
        """
        Check if sample sizes are sufficient.
        
        Args:
            control_size: Control group sample size
            variant_size: Variant group sample size
            minimum: Minimum required sample size per group
        
        Returns:
            True if both groups have sufficient samples
        """
        return control_size >= minimum and variant_size >= minimum

    def determine_winner(
        self,
        control_values: List[float],
        variant_values: List[float],
        confidence_level: float = 0.95,
        minimum_improvement: float = 0.05,
        higher_is_better: bool = True
    ) -> Tuple[Optional[str], float, bool]:
        """
        Determine winning variant.
        
        Args:
            control_values: Control group values
            variant_values: Variant group values
            confidence_level: Required confidence level
            minimum_improvement: Minimum improvement required (e.g., 0.05 = 5%)
            higher_is_better: Whether higher values are better
        
        Returns:
            Tuple of (winner_name, confidence, is_significant)
            winner_name is "control", "variant", or None
        """
        # Calculate means
        control_mean = np.mean(control_values) if control_values else 0.0
        variant_mean = np.mean(variant_values) if variant_values else 0.0

        # Calculate improvement
        if control_mean == 0:
            improvement = 0.0
        else:
            improvement = (variant_mean - control_mean) / control_mean

        # Perform t-test
        _t_stat, p_value = self.calculate_t_test(control_values, variant_values)

        # Check significance
        alpha = 1 - confidence_level
        is_significant = p_value < alpha

        # Determine winner
        winner = None
        confidence = 1 - p_value

        if is_significant:
            # Check if improvement meets minimum threshold
            if higher_is_better:
                if improvement >= minimum_improvement:
                    winner = "variant"
                elif improvement <= -minimum_improvement:
                    winner = "control"
            else:
                # Lower is better (e.g., latency)
                if improvement <= -minimum_improvement:
                    winner = "variant"
                elif improvement >= minimum_improvement:
                    winner = "control"

        return winner, float(confidence), is_significant

    def calculate_sample_size_needed(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        alpha: float = 0.05,
        power: float = 0.8
    ) -> int:
        """
        Calculate required sample size per variant.
        
        Args:
            baseline_rate: Baseline conversion/success rate
            minimum_detectable_effect: Minimum effect to detect (e.g., 0.05 = 5%)
            alpha: Significance level (default: 0.05)
            power: Statistical power (default: 0.8)
        
        Returns:
            Required sample size per variant
        """
        # Z-scores for alpha and power
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)

        # Effect size
        p1 = baseline_rate
        p2 = baseline_rate * (1 + minimum_detectable_effect)

        # Pooled proportion
        p_pool = (p1 + p2) / 2

        # Sample size calculation
        numerator = (z_alpha + z_beta) ** 2 * 2 * p_pool * (1 - p_pool)
        denominator = (p2 - p1) ** 2

        n = math.ceil(numerator / denominator)

        return max(n, 100)  # Minimum 100 samples
