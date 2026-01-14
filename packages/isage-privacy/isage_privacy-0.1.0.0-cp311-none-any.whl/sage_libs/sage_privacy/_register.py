"""Auto-register implementations to SAGE interface.

This module is imported in __init__.py to register all implementations
with the SAGE privacy interface factory.

Note: Registration only happens when sage-libs is installed.
The package can be used standalone without SAGE.
"""

from .dp import GaussianMechanism, LaplaceMechanism
from .unlearning import FisherForgettingUnlearner, GradientAscentUnlearner

# Attempt to register with SAGE interface if available
try:
    from sage.libs.privacy.interface import (
        register_mechanism,
        register_unlearner,
    )

    # ==================== Register Unlearners ====================
    register_unlearner("gradient_ascent", GradientAscentUnlearner)
    register_unlearner("fisher_forgetting", FisherForgettingUnlearner)

    # ==================== Register Privacy Mechanisms ====================
    register_mechanism("gaussian", GaussianMechanism)
    register_mechanism("laplace", LaplaceMechanism)

    _SAGE_REGISTERED = True
except ImportError:
    # SAGE not installed - package can still be used standalone
    _SAGE_REGISTERED = False

__all__ = ["_SAGE_REGISTERED"]
