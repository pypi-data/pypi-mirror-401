"""Dependency injection module."""

from .core import Depends, DependencyScope
from .resolver import DependencyResolver, CircularDependencyError

__all__ = [
    "Depends",
    "DependencyScope",
    "DependencyResolver",
    "CircularDependencyError"
]
