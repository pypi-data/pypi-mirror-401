"""Laplace Mechanism for Differential Privacy.

This module implements the Laplace mechanism for pure ε-differential privacy.
"""

import numpy as np

# Try to import SAGE base class
try:
    from sage.libs.privacy.unlearning.dp_unlearning.base_mechanism import BasePrivacyMechanism

    _HAS_SAGE = True
except ImportError:
    _HAS_SAGE = False
    BasePrivacyMechanism = object  # type: ignore


class LaplaceMechanism(BasePrivacyMechanism):
    """Laplace mechanism for pure ε-differential privacy.

    The Laplace mechanism adds noise drawn from the Laplace distribution
    to achieve pure ε-differential privacy (δ = 0).

    The noise scale is calibrated as:
        b = Δf / ε

    where Δf is the L1 sensitivity of the query.

    The Laplace mechanism is optimal for single numeric queries and
    provides pure differential privacy (no failure probability δ).

    References:
        - Dwork et al. "Calibrating Noise to Sensitivity in Private Data Analysis" (2006)
        - Dwork & Roth "The Algorithmic Foundations of Differential Privacy" (2014)

    Example:
        >>> mechanism = LaplaceMechanism(epsilon=1.0, sensitivity=1.0)
        >>> noise = mechanism.compute_noise()
        >>> private_count = true_count + noise
    """

    def __init__(
        self,
        epsilon: float,
        sensitivity: float = 1.0,
        name: str = "Laplace",
    ):
        """Initialize Laplace mechanism.

        Args:
            epsilon: Privacy parameter (smaller = more private)
            sensitivity: L1 sensitivity of the query
            name: Name of this mechanism

        Raises:
            ValueError: If epsilon <= 0
        """
        if epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {epsilon}")

        # Initialize base class if SAGE available
        if _HAS_SAGE:
            super().__init__(epsilon=epsilon, delta=None, sensitivity=sensitivity, name=name)
        else:
            self.epsilon = epsilon
            self.delta: float | None = None  # Pure DP has no delta
            self.sensitivity = sensitivity
            self.name = name
            self._privacy_spent = 0.0

        # Track queries
        self._num_queries = 0

        # Compute scale parameter
        self._scale = sensitivity / epsilon

    @property
    def scale(self) -> float:
        """Return the Laplace scale parameter (b = Δf/ε)."""
        return self._scale

    def compute_noise(
        self,
        sensitivity: float | None = None,
        epsilon: float | None = None,
        delta: float | None = None,  # Ignored for Laplace
    ) -> float:
        """Generate Laplace noise for differential privacy.

        Args:
            sensitivity: Override default sensitivity
            epsilon: Override default epsilon
            delta: Ignored (Laplace provides pure DP)

        Returns:
            Noise value sampled from Lap(b) where b = Δf/ε
        """
        sens = sensitivity or self.sensitivity
        eps = epsilon or self.epsilon

        scale = sens / eps
        noise = np.random.laplace(0, scale)

        self._num_queries += 1
        self._update_privacy_spent(eps)

        return float(noise)

    def compute_noise_vector(
        self,
        shape: tuple[int, ...],
        sensitivity: float | None = None,
        epsilon: float | None = None,
    ) -> np.ndarray:
        """Generate a vector of Laplace noise.

        Args:
            shape: Shape of the noise vector
            sensitivity: Override default sensitivity
            epsilon: Override default epsilon

        Returns:
            Noise vector sampled from Lap(b)^d
        """
        sens = sensitivity or self.sensitivity
        eps = epsilon or self.epsilon

        scale = sens / eps
        noise = np.random.laplace(0, scale, shape)

        self._num_queries += 1
        self._update_privacy_spent(eps)

        return noise

    def privacy_cost(self) -> tuple[float, float]:
        """Compute the privacy cost of operations so far.

        For pure DP (Laplace), delta is always 0.

        Returns:
            Tuple of (epsilon_spent, delta=0)
        """
        return (self._privacy_spent, 0.0)

    def _update_privacy_spent(self, epsilon: float) -> None:
        """Update privacy budget tracking.

        Uses basic composition: ε_total = Σ ε_i

        Args:
            epsilon: Epsilon for this query
        """
        self._privacy_spent += epsilon

    def perturb_vector(
        self,
        vector: np.ndarray,
        indices_to_perturb: list[int] | None = None,
    ) -> np.ndarray:
        """Perturb a vector with Laplace noise.

        Args:
            vector: Original vector to perturb
            indices_to_perturb: Specific indices to perturb (None = all)

        Returns:
            Perturbed vector
        """
        perturbed = vector.copy()

        if indices_to_perturb is None:
            noise = self.compute_noise_vector(vector.shape)
            perturbed = perturbed + noise
        else:
            for idx in indices_to_perturb:
                noise = self.compute_noise()
                perturbed[idx] += noise

        return perturbed

    def perturb_histogram(
        self,
        histogram: np.ndarray,
        normalize: bool = False,
    ) -> np.ndarray:
        """Perturb a histogram with Laplace noise.

        Histograms are common queries in differential privacy.
        Each bin is perturbed independently.

        Args:
            histogram: Original histogram counts
            normalize: Whether to normalize output to sum to 1

        Returns:
            Perturbed histogram
        """
        noise = self.compute_noise_vector(histogram.shape)
        perturbed = histogram + noise

        # Ensure non-negative counts
        perturbed = np.maximum(perturbed, 0)

        if normalize:
            total = perturbed.sum()
            if total > 0:
                perturbed = perturbed / total

        return perturbed

    def private_sum(
        self,
        values: np.ndarray,
        bounds: tuple[float, float] | None = None,
    ) -> float:
        """Compute a differentially private sum.

        Args:
            values: Array of values to sum
            bounds: Optional (min, max) bounds for clipping

        Returns:
            Private sum with Laplace noise
        """
        if bounds is not None:
            lo, hi = bounds
            values = np.clip(values, lo, hi)
            # Sensitivity is the max contribution
            sens = hi - lo
        else:
            sens = self.sensitivity

        true_sum = float(np.sum(values))
        noise = self.compute_noise(sensitivity=sens)

        return true_sum + noise

    def private_mean(
        self,
        values: np.ndarray,
        bounds: tuple[float, float] | None = None,
    ) -> float:
        """Compute a differentially private mean.

        Args:
            values: Array of values to average
            bounds: Optional (min, max) bounds for clipping

        Returns:
            Private mean with Laplace noise
        """
        n = len(values)
        if n == 0:
            return 0.0

        private_sum = self.private_sum(values, bounds)
        return private_sum / n

    def private_count(
        self,
        predicate: np.ndarray,
    ) -> float:
        """Compute a differentially private count.

        Args:
            predicate: Boolean array indicating items to count

        Returns:
            Private count with Laplace noise
        """
        true_count = float(np.sum(predicate))
        # Sensitivity of count query is 1
        noise = self.compute_noise(sensitivity=1.0)

        return max(0, true_count + noise)

    def get_privacy_guarantee(self) -> dict[str, float]:
        """Get the privacy guarantee of this mechanism.

        Returns:
            Dictionary with 'epsilon' (delta is 0 for pure DP)
        """
        return {
            "epsilon": self.epsilon,
            "delta": 0.0,
            "scale": self._scale,
        }

    def reset_privacy_budget(self) -> None:
        """Reset the privacy budget counter."""
        self._privacy_spent = 0.0
        self._num_queries = 0

    def __repr__(self) -> str:
        return f"{self.name}(ε={self.epsilon}, b={self._scale:.4f})"
