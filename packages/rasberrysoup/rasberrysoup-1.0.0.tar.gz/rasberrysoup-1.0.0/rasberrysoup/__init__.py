import math
import cmath
from typing import List, Tuple, Union

# Golden Ratio Constant
GOLD = 1.6180339887498948482

def quad(a: float, b: float, c: float) -> Tuple[complex, complex]:
    """
    Solves the quadratic equation ax^2 + bx + c = 0.
    Keyword: "quad"
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero.")
    
    # Calculate discriminant
    d = cmath.sqrt(b**2 - 4*a*c)
    
    # Calculate two roots
    sol1 = (-b + d) / (2 * a)
    sol2 = (-b - d) / (2 * a)
    
    return sol1, sol2

def gold() -> float:
    """
    Returns the Golden Ratio value.
    Keyword: "gold"
    """
    return GOLD

def dist(p1: List[float], p2: List[float]) -> float:
    """
    Calculates the Euclidean distance between two points in N-dimensional space.
    Keyword: "dist"
    """
    if len(p1) != len(p2):
        raise ValueError("Vectors must have the same dimension.")
    
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def fourier(input_data: List[float]) -> List[complex]:
    """
    Simplifies Fourier Transform calculation (Discrete version).
    Keyword: "fourier"
    """
    N = len(input_data)
    output = []
    for k in range(N):
        s = complex(0)
        for n in range(N):
            angle = 2.0 * math.pi * k * n / N
            # e^(-i * angle) = cos(angle) - i * sin(angle)
            s += input_data[n] * complex(math.cos(angle), -math.sin(angle))
        output.append(s)
    return output

def interest(principal: float, rate: float, periods: int) -> float:
    """
    Calculates the compound interest.
    Keyword: "interest"
    """
    return principal * (1.0 + rate) ** periods
