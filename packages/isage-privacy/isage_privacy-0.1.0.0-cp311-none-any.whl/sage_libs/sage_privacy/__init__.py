"""SAGE Privacy - Privacy protection and machine unlearning.

This package provides implementations for:
- Machine Unlearning (GradientAscentUnlearner, FisherForgettingUnlearner)
- Differential Privacy (GaussianMechanism, LaplaceMechanism)
- Federated Learning support

Usage:
    # Direct import
    from sage_libs.sage_privacy import GradientAscentUnlearner, GaussianMechanism

    # Or via SAGE factory (after import triggers registration)
    import sage_privacy  # triggers auto-registration
    from sage.libs.privacy.interface import create_unlearner, create_privacy_mechanism
    unlearner = create_unlearner("gradient_ascent")

Installation:
    pip install isage-privacy
"""

# Auto-register implementations to SAGE interface
from . import _register  # noqa: F401
from ._version import __author__, __email__, __version__
from .dp import GaussianMechanism, LaplaceMechanism

# Re-export main implementations
from .unlearning import FisherForgettingUnlearner, GradientAscentUnlearner

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Unlearning
    "GradientAscentUnlearner",
    "FisherForgettingUnlearner",
    # Differential Privacy
    "GaussianMechanism",
    "LaplaceMechanism",
]
