"""Gaussian Mechanism for Differential Privacy.

This module implements the Gaussian mechanism for (ε,δ)-differential privacy.
"""

from dataclasses import dataclass

import numpy as np

# Try to import SAGE base class
try:
    from sage.libs.privacy.unlearning.dp_unlearning.base_mechanism import BasePrivacyMechanism

    _HAS_SAGE = True
except ImportError:
    _HAS_SAGE = False
    BasePrivacyMechanism = object  # type: ignore


@dataclass
class GaussianNoiseParams:
    """Parameters for Gaussian noise computation."""

    sigma: float  # Standard deviation
    epsilon: float
    delta: float
    sensitivity: float


class GaussianMechanism(BasePrivacyMechanism):
    """Gaussian mechanism for (ε,δ)-differential privacy.

    The Gaussian mechanism adds Gaussian noise calibrated to achieve
    (ε,δ)-differential privacy. It provides better utility than the
    Laplace mechanism when δ > 0 is acceptable.

    The noise scale is calibrated as:
        σ = Δf * sqrt(2 * ln(1.25/δ)) / ε

    where Δf is the L2 sensitivity of the query.

    References:
        - Dwork & Roth "The Algorithmic Foundations of Differential Privacy" (2014)
        - Mironov "On Significance of the Least Significant Bits For Differential Privacy" (2012)

    Example:
        >>> mechanism = GaussianMechanism(epsilon=1.0, delta=1e-5, sensitivity=1.0)
        >>> noise = mechanism.compute_noise()
        >>> private_value = true_value + noise
    """

    def __init__(
        self,
        epsilon: float,
        delta: float = 1e-5,
        sensitivity: float = 1.0,
        name: str = "Gaussian",
    ):
        """Initialize Gaussian mechanism.

        Args:
            epsilon: Privacy parameter (smaller = more private)
            delta: Failure probability (must be in (0, 1))
            sensitivity: L2 sensitivity of the query
            name: Name of this mechanism

        Raises:
            ValueError: If epsilon <= 0 or delta not in (0, 1)
        """
        if epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {epsilon}")
        if not (0 < delta < 1):
            raise ValueError(f"delta must be in (0, 1), got {delta}")

        # Initialize base class if SAGE available
        if _HAS_SAGE:
            super().__init__(epsilon=epsilon, delta=delta, sensitivity=sensitivity, name=name)
        else:
            self.epsilon = epsilon
            self.delta = delta
            self.sensitivity = sensitivity
            self.name = name
            self._privacy_spent = 0.0

        # Track queries
        self._num_queries = 0

        # Compute sigma
        self._sigma = self._compute_sigma(epsilon, delta, sensitivity)

    def _compute_sigma(
        self,
        epsilon: float,
        delta: float,
        sensitivity: float,
    ) -> float:
        """Compute the standard deviation for Gaussian noise.

        The formula is: σ = Δf * sqrt(2 * ln(1.25/δ)) / ε

        Args:
            epsilon: Privacy parameter
            delta: Failure probability
            sensitivity: L2 sensitivity

        Returns:
            Standard deviation sigma
        """
        return sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / epsilon

    @property
    def sigma(self) -> float:
        """Return the noise standard deviation."""
        return self._sigma

    def compute_noise(
        self,
        sensitivity: float | None = None,
        epsilon: float | None = None,
        delta: float | None = None,
    ) -> float:
        """Generate Gaussian noise for differential privacy.

        Args:
            sensitivity: Override default sensitivity
            epsilon: Override default epsilon
            delta: Override default delta

        Returns:
            Noise value sampled from N(0, σ²)
        """
        sens = sensitivity or self.sensitivity
        eps = epsilon or self.epsilon
        dlt = delta or self.delta

        if eps != self.epsilon or dlt != self.delta or sens != self.sensitivity:
            sigma = self._compute_sigma(eps, dlt, sens)
        else:
            sigma = self._sigma

        noise = np.random.normal(0, sigma)
        self._num_queries += 1
        self._update_privacy_spent(eps, dlt)

        return float(noise)

    def compute_noise_vector(
        self,
        shape: tuple[int, ...],
        sensitivity: float | None = None,
        epsilon: float | None = None,
        delta: float | None = None,
    ) -> np.ndarray:
        """Generate a vector of Gaussian noise.

        Args:
            shape: Shape of the noise vector
            sensitivity: Override default sensitivity
            epsilon: Override default epsilon
            delta: Override default delta

        Returns:
            Noise vector sampled from N(0, σ²I)
        """
        sens = sensitivity or self.sensitivity
        eps = epsilon or self.epsilon
        dlt = delta or self.delta

        if eps != self.epsilon or dlt != self.delta or sens != self.sensitivity:
            sigma = self._compute_sigma(eps, dlt, sens)
        else:
            sigma = self._sigma

        noise = np.random.normal(0, sigma, shape)
        self._num_queries += 1
        self._update_privacy_spent(eps, dlt)

        return noise

    def privacy_cost(self) -> tuple[float, float]:
        """Compute the privacy cost of operations so far.

        Returns:
            Tuple of (epsilon_spent, delta_spent)
        """
        return (self._privacy_spent, self.delta * self._num_queries)

    def _update_privacy_spent(self, epsilon: float, delta: float) -> None:
        """Update privacy budget tracking.

        Uses basic composition for simplicity.
        Advanced composition can provide tighter bounds.

        Args:
            epsilon: Epsilon for this query
            delta: Delta for this query
        """
        # Basic composition: ε_total = Σ ε_i
        self._privacy_spent += epsilon

    def perturb_vector(
        self,
        vector: np.ndarray,
        indices_to_perturb: list[int] | None = None,
    ) -> np.ndarray:
        """Perturb a vector with Gaussian noise.

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

    def perturb_matrix(
        self,
        matrix: np.ndarray,
        row_sensitivity: float | None = None,
    ) -> np.ndarray:
        """Perturb a matrix with Gaussian noise.

        For matrices, we can have different sensitivity notions:
        - Entry-wise sensitivity
        - Row sensitivity
        - Spectral sensitivity

        Args:
            matrix: Original matrix to perturb
            row_sensitivity: Per-row L2 sensitivity (optional)

        Returns:
            Perturbed matrix
        """
        sens = row_sensitivity or self.sensitivity
        sigma = self._compute_sigma(self.epsilon, self.delta, sens)

        noise = np.random.normal(0, sigma, matrix.shape)
        self._num_queries += 1
        self._update_privacy_spent(self.epsilon, self.delta)

        return matrix + noise

    def get_privacy_guarantee(self) -> dict[str, float]:
        """Get the privacy guarantee of this mechanism.

        Returns:
            Dictionary with 'epsilon' and 'delta'
        """
        return {
            "epsilon": self.epsilon,
            "delta": self.delta,
            "sigma": self._sigma,
        }

    def reset_privacy_budget(self) -> None:
        """Reset the privacy budget counter."""
        self._privacy_spent = 0.0
        self._num_queries = 0

    def get_noise_params(self) -> GaussianNoiseParams:
        """Get the noise parameters.

        Returns:
            GaussianNoiseParams with current settings
        """
        return GaussianNoiseParams(
            sigma=self._sigma,
            epsilon=self.epsilon,
            delta=self.delta,
            sensitivity=self.sensitivity,
        )

    def __repr__(self) -> str:
        return f"{self.name}(ε={self.epsilon}, δ={self.delta}, σ={self._sigma:.4f})"
