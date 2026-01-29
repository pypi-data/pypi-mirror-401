"""
Unit testing suite for the Vecture String-Pi library.

Ensures mathematical correctness and convergence behaviors of the
Saha-Sinha implementation.
"""

import mpmath
import pytest
from string_pi.core import calculate_pi

def test_convergence_large_lambda():
    """
    Verifies that the Saha-Sinha algorithm converges toward Pi for large Lambda values.
    
    This test validates the asymptotic behavior where the series reduces to
    stable geometric approximations.
    """
    target = mpmath.pi
    
    # High lambda values require substantial iteration depth for high precision,
    # but we check for general alignment here to confirm formula stability.
    res = calculate_pi(iterations=5000, lambda_val=10**6)
    
    # Assert convergence within a reasonable tolerance for this parameter set
    assert mpmath.absmin(res - target) < 1e-3

def test_precision_increase():
    """
    Verifies that increasing iteration depth yields higher precision.
    
    This confirms that the series is effectively converging and not oscillating
    or diverging for standard parameters.
    """
    lam = 1000.0
    error_10 = mpmath.absmin(calculate_pi(10, lam) - mpmath.pi)
    error_100 = mpmath.absmin(calculate_pi(100, lam) - mpmath.pi)
    
    # The error at 100 iterations must be strictly less than at 10 iterations
    assert error_100 < error_10