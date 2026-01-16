# 🍧 Rasberrysoup

![Rasberrysoup Logo](assets/logo.png)

**Rasberrysoup** is a professional Python library designed to simplify complex mathematical operations into intuitive keyword-based function calls. Originally a C++ library, it has been reimagined and ported to Python to provide high-performance implementations for common engineering and scientific tasks.

## ✨ Key Features

- **Quadratic Solver (`quad`)**: Solve $ax^2 + bx + c = 0$ with complex root support.
- **Golden Ratio (`gold`)**: High-precision constant for aesthetic and mathematical design.
- **Fourier Transform (`fourier`)**: Simplified discrete transform for signal analysis.
- **Euclidean Distance (`dist`)**: Multi-dimensional distance calculations.
- **Compound Interest (`interest`)**: Fast financial growth modeling.

## 🚀 Installation

You can install Rasberrysoup directly from the source:

```bash
pip install .
```

## 🔧 Usage

```python
from rasberrysoup import quad, gold, dist

# 1. Golden Ratio
print(f"Golden Ratio: {gold()}")

# 2. Quadratic Solver (x^2 - 5x + 6 = 0)
roots = quad(1, -5, 6)
print(f"Roots: {roots}")

# 3. Distance Calculation
d = dist([0, 0], [3, 4])
print(f"Distance: {d}")
```

---
**Author:** Rheehose (Rhee Creative)
**Copyright:** © 2008-2026
**License:** MIT
