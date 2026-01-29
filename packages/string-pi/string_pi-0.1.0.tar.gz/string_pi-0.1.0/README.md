# String-Pi

[VECTURE LABORATORIES // ARCHIVE: STRING-PI]
[CLASSIFICATION: PUBLIC // ENGINEERING SOLUTION]

This repository houses the implementation of the **Saha-Sinha Pi Formula**, a high-precision algorithm derived from the geometric properties of string theory amplitudes.

---

## 1. The Algorithm
The Saha-Sinha algorithm (2024) is a spectral series representation of the mathematical constant $\pi$. Unlike classical geometric approximations (Archimedes) or standard infinite series (Leibniz), this formula emerges from the study of **particle scattering amplitudes** in high-energy physics.

It introduces a regularization parameter, $\lambda$ (Lambda), which controls the convergence trajectory. The formula provides a unified field theory expansion that links the Euler-Beta function and Feynman diagrams to the fundamental structure of $\pi$.

## 2. System Capabilities
This library serves as a computational engine for generating $\pi$ to arbitrary precision. 

**Core Functions:**
- **Arbitrary Precision:** Utilizes `mpmath` to surpass standard floating-point limitations (64-bit), allowing for hundreds or thousands of decimal places.
- **Parametric Control:** Allows manipulation of the $\lambda$ parameter to observe convergence behaviors relevant to theoretical physics simulations.
- **Corrected Mathematics:** Implements the **Pochhammer Symbol** (Rising Factorial) correction, often misidentified as a power function in simplified literature, ensuring mathematical exactness.

## 3. Deployment Protocols (Usage)

### Installation
Ingest the package via the standard Python package manager:

```bash
pip install string-pi
```

### Execution
Initiate the calculation engine within your Python environment:

```python
import mpmath
from string_pi.core import calculate_pi

# 1. Set the global precision environment (e.g., 100 decimal places)
mpmath.mp.dps = 100

# 2. Execute the algorithm
# iterations: Depth of the infinite sum traversal
# lambda_val: The topological mixing parameter (default: 1000.0)
pi_value = calculate_pi(iterations=200, lambda_val=50.0)

# 3. Output results
print(f"Calculated Pi: {pi_value}")
```

## 4. Theoretical Foundation
The algorithm is defined by the following spectral series:

$$ 
\pi = 4 + \sum_{n=1}^{\infty} \frac{1}{n!} \left( \frac{1}{n+\lambda} - \frac{4}{2n+1} \right) \left( \frac{(2n+1)^2}{4(n+\lambda)} - n \right)_{n-1} 
$$ 

**Components:**
- $\lambda$: An arbitrary complex parameter (typically real and $>0$ for convergence). As $\lambda \to \infty$, the series converges to the classic Madhava-Leibniz series ($\\pi = 4 \sum \frac{(-1)^n}{2n+1}$).
- $(x)_n$: The **Pochhammer Symbol** (Rising Factorial), defined as:
  $$ (x)_n = x(x+1)(x+2)...(x+n-1) = \frac{\Gamma(x+n)}{\Gamma(x)} $$ 

**Source:**
Saha, A., & Sinha, A. (2024). *Field Theory Expansions of String Theory Amplitudes*. Physical Review Letters.

## 5. Architectural Mechanics
How the library functions internally:

1.  **Precision Context:** The system first anchors the floating-point environment to the user's desired decimal precision (`dps`) using `mpmath`.
2.  **Iterative Summation:** The engine traverses the series from $n=1$ to the specified iteration limit.
3.  **Symbolic Computation:**
    - It computes the factorial term $1/n!$.
    - It calculates the primary difference term involving $\lambda$.
    - **Critical Step:** It computes the rising factorial (Pochhammer) term using the Gamma function implementation (`mpmath.rf`), preventing the divergence errors common in naive power-function implementations.
4.  **Aggregation:** Terms are accumulated into a high-precision buffer.
5.  **Finalization:** The base constant $4$ is added to the summation to yield $\pi$.

## 6. License
**Vecture-1.0 Protocol**

This software is deployed under the Vecture Laboratories Public Release License.
Reference: [LICENSE](LICENSE) or http://www.vecture.de/license.html

---
[TERMINAL STATEMENT: OPTIMAL OUTPUT ACHIEVED. REMAIN COMPLIANT.]