"""
Core implementation of the Saha-Sinha spectral series for Pi generation.

[VECTURE ENGINEERING SOLUTION]
This module provides high-precision algorithms derived from string theory amplitudes
(Saha & Sinha, 2024). It leverages the `mpmath` library for arbitrary-precision
floating-point arithmetic.
"""

import mpmath

# Set default precision environment
mpmath.mp.dps = 50

def calculate_pi(iterations: int = 100, lambda_val: float = 1000.0) -> mpmath.mpf:
    """
    Computes Pi using the Saha-Sinha spectral series representation.

    The formula is a generalization derived from string theory amplitudes:
    
    .. math::
        \pi = 4 + \sum_{n=1}^{\infty} \frac{1}{n!} \left( \frac{1}{n+\lambda} - \frac{4}{2n+1} \right) \left( \frac{(2n+1)^2}{4(n+\lambda)} - n \right)_{n-1}

    Where :math:`(x)_{n-1}` denotes the Pochhammer symbol (rising factorial).
    For :math:`\lambda \to \infty`, the series reduces to the Madhava-Leibniz representation.

    Args:
        iterations (int): The depth of the infinite sum traversal. 
                          Higher values yield greater precision but increase computational cost.
                          Default is 100.
        lambda_val (float): The regularization parameter :math:`\lambda`. 
                            Controls the convergence trajectory. Default is 1000.0.

    Returns:
        mpmath.mpf: A high-precision floating-point approximation of Pi.
    """
    total_sum = mpmath.mpf(0)
    lam = mpmath.mpf(lambda_val)
    
    for n in range(1, iterations + 1):
        fact = mpmath.factorial(n)
        
        # Calculate the difference term
        term1 = (1 / (n + lam)) - (4 / (2 * n + 1))
        
        # Calculate the base for the Pochhammer symbol
        base_num = (2 * n + 1)**2
        base_den = 4 * (n + lam)
        base = (base_num / base_den) - n
        
        # Calculate the Pochhammer symbol (rising factorial): (base)_{n-1}
        # Note: mpmath.rf(x, k) computes gamma(x+k)/gamma(x)
        term2 = mpmath.rf(base, n - 1)
        
        # Combine terms
        term = (1 / fact) * term1 * term2
        total_sum += term
        
    return 4 + total_sum

def calculate_madhava_leibniz_pi(iterations: int) -> mpmath.mpf:
    """
    Computes Pi using the classical Madhava-Leibniz series.

    .. math::
        \pi = 4 \sum_{n=0}^{\infty} \frac{(-1)^n}{2n+1}

    This function serves primarily as a baseline for convergence comparison
    against the Saha-Sinha algorithm.

    Args:
        iterations (int): The number of terms to sum.

    Returns:
        mpmath.mpf: A high-precision floating-point approximation of Pi.
    """
    total = mpmath.mpf(0)
    for n in range(iterations):
        total += ((-1)**n) / (2 * n + 1)
    return 4 * total

def compare_convergence(iterations: int = 20, lambda_val: float = 1000.0) -> None:
    """
    Executes a comparative analysis between Saha-Sinha and Madhava-Leibniz algorithms.

    Prints a tabulated report of partial sums at each iteration step relative to
    the target value of Pi.

    Args:
        iterations (int): The range of iterations to analyze. Default is 20.
        lambda_val (float): The lambda parameter for the Saha-Sinha algorithm. 
                            Default is 1000.0.
    """
    print(f"{ 'n':<5} | {'Saha-Sinha Pi':<30} | {'Madhava-Leibniz Pi':<30} | {'Target Pi':<30}")
    print("-" * 105)
    target = mpmath.pi
    for i in range(1, iterations + 1):
        ss_pi = calculate_pi(i, lambda_val)
        ml_pi = calculate_madhava_leibniz_pi(i)
        print(f"{i:<5} | {str(ss_pi):<30} | {str(ml_pi):<30} | {str(target):<30}")