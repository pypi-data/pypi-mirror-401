"""
Statistical tests for drift detection.
"""

import numpy as np
from scipy import stats
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class StatisticalTests:
    """
    Statistical tests for drift detection.
    
    Provides methods for detecting distribution changes using various
    statistical tests.
    """

    @staticmethod
    def kolmogorov_smirnov(
        baseline: np.ndarray,
        current: np.ndarray
    ) -> Tuple[float, float]:
        """
        Kolmogorov-Smirnov test for numerical features.
        
        Tests whether two samples come from the same distribution.
        
        Args:
            baseline: Baseline data
            current: Current data
        
        Returns:
            Tuple of (ks_statistic, p_value)
            
        Interpretation:
            - p_value > 0.05: No significant drift
            - p_value <= 0.05: Significant drift detected
        """
        if len(baseline) < 2 or len(current) < 2:
            return 0.0, 1.0

        ks_stat, p_value = stats.ks_2samp(baseline, current)
        return float(ks_stat), float(p_value)

    @staticmethod
    def population_stability_index(
        baseline: np.ndarray,
        current: np.ndarray,
        bins: int = 10
    ) -> float:
        """
        Population Stability Index (PSI) for numerical features.
        
        PSI measures the shift in distribution between two datasets.
        
        Args:
            baseline: Baseline data
            current: Current data
            bins: Number of bins for histogram
        
        Returns:
            PSI score
            
        Interpretation:
            - PSI < 0.1: No significant drift
            - 0.1 <= PSI < 0.2: Moderate drift
            - PSI >= 0.2: Significant drift
        """
        if len(baseline) < 2 or len(current) < 2:
            return 0.0

        # Create bins based on baseline
        min_val = min(baseline.min(), current.min())
        max_val = max(baseline.max(), current.max())

        # Handle edge case where all values are the same
        if min_val == max_val:
            return 0.0

        bin_edges = np.linspace(min_val, max_val, bins + 1)

        # Calculate distributions
        baseline_dist, _ = np.histogram(baseline, bins=bin_edges)
        current_dist, _ = np.histogram(current, bins=bin_edges)

        # Convert to percentages
        baseline_pct = baseline_dist / len(baseline)
        current_pct = current_dist / len(current)

        # Avoid division by zero
        baseline_pct = np.where(baseline_pct == 0, 0.0001, baseline_pct)
        current_pct = np.where(current_pct == 0, 0.0001, current_pct)

        # Calculate PSI
        psi = np.sum((current_pct - baseline_pct) * np.log(current_pct / baseline_pct))

        return float(psi)

    @staticmethod
    def jensen_shannon_divergence(
        baseline: np.ndarray,
        current: np.ndarray,
        bins: int = 10
    ) -> float:
        """
        Jensen-Shannon divergence for distributions.
        
        Measures similarity between two probability distributions.
        
        Args:
            baseline: Baseline data
            current: Current data
            bins: Number of bins for histogram
        
        Returns:
            JS divergence (0 to 1, where 0 = identical)
        """
        if len(baseline) < 2 or len(current) < 2:
            return 0.0

        # Create bins
        min_val = min(baseline.min(), current.min())
        max_val = max(baseline.max(), current.max())

        if min_val == max_val:
            return 0.0

        bin_edges = np.linspace(min_val, max_val, bins + 1)

        # Calculate distributions
        baseline_dist, _ = np.histogram(baseline, bins=bin_edges)
        current_dist, _ = np.histogram(current, bins=bin_edges)

        # Normalize to probabilities
        p = baseline_dist / baseline_dist.sum()
        q = current_dist / current_dist.sum()

        # Avoid log(0)
        p = np.where(p == 0, 1e-10, p)
        q = np.where(q == 0, 1e-10, q)

        # Calculate JS divergence
        m = 0.5 * (p + q)
        js_div = 0.5 * stats.entropy(p, m) + 0.5 * stats.entropy(q, m)

        return float(js_div)

    @staticmethod
    def chi_square_categorical(
        baseline_counts: Dict[str, int],
        current_counts: Dict[str, int]
    ) -> Tuple[float, float]:
        """
        Chi-square test for categorical features.
        
        Tests whether the distribution of categories has changed.
        
        Args:
            baseline_counts: Category counts in baseline
            current_counts: Category counts in current data
        
        Returns:
            Tuple of (chi2_statistic, p_value)
        """
        # Get all categories
        all_categories = set(baseline_counts.keys()) | set(current_counts.keys())

        if len(all_categories) < 2:
            return 0.0, 1.0

        # Build contingency table
        baseline_list = [baseline_counts.get(cat, 0) for cat in all_categories]
        current_list = [current_counts.get(cat, 0) for cat in all_categories]

        # Perform chi-square test
        contingency_table = np.array([baseline_list, current_list])

        try:
            chi2, p_value, _dof, _expected = stats.chi2_contingency(contingency_table)
            return float(chi2), float(p_value)
        except ValueError:
            # Not enough data
            return 0.0, 1.0

    @staticmethod
    def classify_drift_severity(
        psi_score: float,
        ks_p_value: float = None
    ) -> str:
        """
        Classify drift severity based on PSI and KS test.
        
        Args:
            psi_score: PSI score
            ks_p_value: Optional KS test p-value
        
        Returns:
            Severity level: 'none', 'low', 'medium', 'high', 'critical'
        """
        # Primary classification based on PSI
        if psi_score < 0.1:
            severity = 'none'
        elif psi_score < 0.15:
            severity = 'low'
        elif psi_score < 0.2:
            severity = 'medium'
        elif psi_score < 0.3:
            severity = 'high'
        else:
            severity = 'critical'

        # Adjust based on KS test if available
        if ks_p_value is not None:
            if ks_p_value < 0.01 and severity in ['none', 'low']:
                severity = 'medium'
            elif ks_p_value < 0.001 and severity == 'medium':
                severity = 'high'

        return severity
