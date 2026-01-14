"""
Assignment strategies for A/B testing.
"""

import hashlib
import random
from abc import ABC, abstractmethod
from typing import List

from neuralforge.db.models.ab_variant import ABVariant


class AssignmentStrategy(ABC):
    """Base class for assignment strategies."""

    @abstractmethod
    def assign(self, user_id: str, variants: List[ABVariant]) -> ABVariant:
        """
        Assign user to a variant.
        
        Args:
            user_id: User identifier
            variants: List of active variants
        
        Returns:
            Assigned variant
        """
        pass


class UserHashAssignment(AssignmentStrategy):
    """
    Consistent hash-based assignment.
    
    Uses MD5 hash of user_id to deterministically assign users to variants.
    Ensures same user always gets same variant.
    """

    def assign(self, user_id: str, variants: List[ABVariant]) -> ABVariant:
        """Assign user based on hash of user_id."""
        # Hash user_id
        hash_value = hashlib.md5(user_id.encode()).hexdigest()
        hash_int = int(hash_value, 16)

        # Convert to 0-100 range
        hash_percent = (hash_int % 10000) / 100.0

        # Assign based on traffic allocation
        cumulative = 0.0
        for variant in sorted(variants, key=lambda v: v.id):  # Sort for consistency
            cumulative += variant.traffic_percentage
            if hash_percent < cumulative:
                return variant

        # Fallback to last variant (shouldn't happen if traffic sums to 100)
        return variants[-1]


class RandomAssignment(AssignmentStrategy):
    """
    Random assignment based on traffic percentages.
    
    Each request gets a random assignment. Not sticky - same user
    may get different variants on different requests.
    """

    def assign(self, user_id: str, variants: List[ABVariant]) -> ABVariant:
        """Assign user randomly based on traffic percentages."""
        rand_percent = random.random() * 100

        cumulative = 0.0
        for variant in variants:
            cumulative += variant.traffic_percentage
            if rand_percent < cumulative:
                return variant

        # Fallback
        return variants[-1]


class StickyRandomAssignment(AssignmentStrategy):
    """
    Random assignment with stickiness.
    
    First assignment is random, but subsequent assignments for the
    same user are consistent (stored in database).
    """

    def assign(self, user_id: str, variants: List[ABVariant]) -> ABVariant:
        """
        Assign user randomly.
        
        Note: Stickiness is handled by ExperimentManager checking
        for existing assignments before calling this method.
        """
        return RandomAssignment().assign(user_id, variants)


def get_assignment_strategy(strategy_name: str) -> AssignmentStrategy:
    """
    Get assignment strategy by name.
    
    Args:
        strategy_name: Strategy name (user_hash, random, sticky)
    
    Returns:
        Assignment strategy instance
    """
    strategies = {
        "user_hash": UserHashAssignment(),
        "random": RandomAssignment(),
        "sticky": StickyRandomAssignment(),
    }

    return strategies.get(strategy_name, UserHashAssignment())
