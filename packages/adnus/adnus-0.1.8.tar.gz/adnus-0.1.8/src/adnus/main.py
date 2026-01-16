# src/adnus/main.py
"""
adnus (AdNuS): A Python library for Advanced Number Systems.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from fractions import Fraction
import math
from typing import List, Union, Generator, Tuple, Any
from hypercomplex import reals, Complex, Quaternion, Octonion, Sedenion, Pathion, Chingon, Routon, Voudon, cayley_dickson_construction, cayley_dickson_algebra

class AdvancedNumber(ABC):
    """Abstract Base Class for advanced number systems."""

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


@dataclass(frozen=True)
class BicomplexNumber(AdvancedNumber):
    """
    Represents a bicomplex number z = z1 + z2j, where z1 and z2 are complex
    numbers and j^2 = -1, but j is an independent imaginary unit from i.
    """
    z1: Complex
    z2: Complex

    def __init__(self, z1: Union[Complex, complex, float, int], 
                 z2: Union[Complex, complex, float, int]):
        # Convert inputs to Complex type if needed
        if not isinstance(z1, Complex):
            z1 = Complex(z1)
        if not isinstance(z2, Complex):
            z2 = Complex(z2)
        object.__setattr__(self, 'z1', z1)
        object.__setattr__(self, 'z2', z2)

    def __add__(self, other: BicomplexNumber) -> BicomplexNumber:
        if not isinstance(other, BicomplexNumber):
            return NotImplemented
        return BicomplexNumber(self.z1 + other.z1, self.z2 + other.z2)

    def __sub__(self, other: BicomplexNumber) -> BicomplexNumber:
        if not isinstance(other, BicomplexNumber):
            return NotImplemented
        return BicomplexNumber(self.z1 - other.z1, self.z2 - other.z2)

    def __mul__(self, other: Union[BicomplexNumber, float, int, complex, Complex]) -> BicomplexNumber:
        if isinstance(other, (float, int, complex, Complex)):
            return BicomplexNumber(self.z1 * other, self.z2 * other)
        if not isinstance(other, BicomplexNumber):
            return NotImplemented
        # (z1 + z2j)(w1 + w2j) = (z1w1 - z2w2) + (z1w2 + z2w1)j
        return BicomplexNumber(
            self.z1 * other.z1 - self.z2 * other.z2,
            self.z1 * other.z2 + self.z2 * other.z1
        )

    def __truediv__(self, other: BicomplexNumber) -> BicomplexNumber:
        # Division using the conjugate approach
        if isinstance(other, (float, int, complex, Complex)):
            return BicomplexNumber(self.z1 / other, self.z2 / other)
        
        if not isinstance(other, BicomplexNumber):
            return NotImplemented
        
        # Compute the conjugate of the denominator
        conjugate = BicomplexNumber(other.z1, -other.z2)
        
        # Multiply numerator and denominator by conjugate
        numerator = self * conjugate
        denominator = other * conjugate
        
        # Denominator should be a real number (only z1 component)
        if abs(denominator.z2.real) > 1e-10 or abs(denominator.z2.imag) > 1e-10:
            raise ValueError("Division resulted in non-real denominator")
            
        return BicomplexNumber(numerator.z1 / denominator.z1.real, 
                              numerator.z2 / denominator.z1.real)

    def __eq__(self, other) -> bool:
        if not isinstance(other, BicomplexNumber):
            return NotImplemented
        return self.z1 == other.z1 and self.z2 == other.z2

    def __repr__(self) -> str:
        return f"({self.z1}) + ({self.z2})j"

    def norm(self) -> float:
        """Returns the Euclidean norm of the bicomplex number."""
        return math.sqrt(abs(self.z1)**2 + abs(self.z2)**2)


@dataclass(frozen=True)
class NeutrosophicNumber(AdvancedNumber):
    """
    Represents a neutrosophic number z = a + bI, where 'a' is the determinate part,
    'b' is the indeterminate part, and I is the indeterminacy, satisfying I^2 = I.
    """
    a: Union[float, int, Fraction]
    b: Union[float, int, Fraction]

    def __add__(self, other: NeutrosophicNumber) -> NeutrosophicNumber:
        if not isinstance(other, NeutrosophicNumber):
            return NotImplemented
        return NeutrosophicNumber(self.a + other.a, self.b + other.b)

    def __sub__(self, other: NeutrosophicNumber) -> NeutrosophicNumber:
        if not isinstance(other, NeutrosophicNumber):
            return NotImplemented
        return NeutrosophicNumber(self.a - other.a, self.b - other.b)

    def __mul__(self, other: NeutrosophicNumber) -> NeutrosophicNumber:
        if not isinstance(other, NeutrosophicNumber):
            return NotImplemented
        # (a + bI)(c + dI) = ac + (ad + bc + bd)I
        return NeutrosophicNumber(
            self.a * other.a,
            self.a * other.b + self.b * other.a + self.b * other.b
        )

    def __truediv__(self, other: NeutrosophicNumber) -> NeutrosophicNumber:
        # Division using the conjugate approach
        if not isinstance(other, NeutrosophicNumber):
            return NotImplemented
        
        # Compute conjugate (a - bI)
        conjugate = NeutrosophicNumber(other.a, -other.b)
        
        # Multiply numerator and denominator by conjugate
        numerator = self * conjugate
        denominator = other * conjugate
        
        # Denominator should be a real number (only a component)
        if abs(denominator.b) > 1e-10:
            raise ValueError("Division resulted in non-real denominator")
            
        return NeutrosophicNumber(numerator.a / denominator.a, 
                                 numerator.b / denominator.a)

    def __eq__(self, other) -> bool:
        if not isinstance(other, NeutrosophicNumber):
            return NotImplemented
        return self.a == other.a and self.b == other.b

    def __repr__(self) -> str:
        return f"{self.a} + {self.b}I"


@dataclass(frozen=True)
class NeutrosophicComplexNumber(AdvancedNumber):
    """
    Represents a neutrosophic complex number z = (a + bi) + (c + di)I.
    This can be seen as a neutrosophic number whose determinate and indeterminate
    parts are complex numbers.
    """
    determinate: Complex
    indeterminate: Complex

    def __init__(self, determinate: Union[Complex, complex, float, int], 
                 indeterminate: Union[Complex, complex, float, int]):
        # Convert inputs to Complex type if needed
        if not isinstance(determinate, Complex):
            determinate = Complex(determinate)
        if not isinstance(indeterminate, Complex):
            indeterminate = Complex(indeterminate)
        object.__setattr__(self, 'determinate', determinate)
        object.__setattr__(self, 'indeterminate', indeterminate)

    def __add__(self, other: NeutrosophicComplexNumber) -> NeutrosophicComplexNumber:
        if not isinstance(other, NeutrosophicComplexNumber):
            return NotImplemented
        return NeutrosophicComplexNumber(
            self.determinate + other.determinate,
            self.indeterminate + other.indeterminate
        )

    def __sub__(self, other: NeutrosophicComplexNumber) -> NeutrosophicComplexNumber:
        if not isinstance(other, NeutrosophicComplexNumber):
            return NotImplemented
        return NeutrosophicComplexNumber(
            self.determinate - other.determinate,
            self.indeterminate - other.indeterminate
        )

    def __mul__(self, other: NeutrosophicComplexNumber) -> NeutrosophicComplexNumber:
        if not isinstance(other, NeutrosophicComplexNumber):
            return NotImplemented
        # (A + BI)(C + DI) = AC + (AD + BC + BD)I, where A, B, C, D are complex.
        determinate_part = self.determinate * other.determinate
        indeterminate_part = (self.determinate * other.indeterminate +
                              self.indeterminate * other.determinate +
                              self.indeterminate * other.indeterminate)
        return NeutrosophicComplexNumber(determinate_part, indeterminate_part)

    def __truediv__(self, other: NeutrosophicComplexNumber) -> NeutrosophicComplexNumber:
        # Division using the conjugate approach
        if not isinstance(other, NeutrosophicComplexNumber):
            return NotImplemented
        
        # Compute conjugate (C - DI)
        conjugate = NeutrosophicComplexNumber(other.determinate, -other.indeterminate)
        
        # Multiply numerator and denominator by conjugate
        numerator = self * conjugate
        denominator = other * conjugate
        
        # Denominator should be a complex number (only determinate part)
        if abs(denominator.indeterminate.real) > 1e-10 or abs(denominator.indeterminate.imag) > 1e-10:
            raise ValueError("Division resulted in non-complex denominator")
            
        return NeutrosophicComplexNumber(numerator.determinate / denominator.determinate, 
                                        numerator.indeterminate / denominator.determinate)

    def __eq__(self, other) -> bool:
        if not isinstance(other, NeutrosophicComplexNumber):
            return NotImplemented
        return self.determinate == other.determinate and self.indeterminate == other.indeterminate

    def __repr__(self) -> str:
        return f"({self.determinate}) + ({self.indeterminate})I"


@dataclass(frozen=True)
class NeutrosophicBicomplexNumber(AdvancedNumber):
    """
    Represents a neutrosophic bicomplex number z = (z1 + z2j) + (w1 + w2j)I.
    This can be seen as a neutrosophic number whose determinate and indeterminate
    parts are bicomplex numbers.
    """
    determinate: BicomplexNumber
    indeterminate: BicomplexNumber

    def __add__(self, other: NeutrosophicBicomplexNumber) -> NeutrosophicBicomplexNumber:
        if not isinstance(other, NeutrosophicBicomplexNumber):
            return NotImplemented
        return NeutrosophicBicomplexNumber(
            self.determinate + other.determinate,
            self.indeterminate + other.indeterminate
        )

    def __sub__(self, other: NeutrosophicBicomplexNumber) -> NeutrosophicBicomplexNumber:
        if not isinstance(other, NeutrosophicBicomplexNumber):
            return NotImplemented
        return NeutrosophicBicomplexNumber(
            self.determinate - other.determinate,
            self.indeterminate - other.indeterminate
        )

    def __mul__(self, other: NeutrosophicBicomplexNumber) -> NeutrosophicBicomplexNumber:
        if not isinstance(other, NeutrosophicBicomplexNumber):
            return NotImplemented
        # (A + BI)(C + DI) = AC + (AD + BC + BD)I, where A, B, C, D are bicomplex.
        determinate_part = self.determinate * other.determinate
        indeterminate_part = (self.determinate * other.indeterminate +
                              self.indeterminate * other.determinate +
                              self.indeterminate * other.indeterminate)
        return NeutrosophicBicomplexNumber(determinate_part, indeterminate_part)

    def __truediv__(self, other: NeutrosophicBicomplexNumber) -> NeutrosophicBicomplexNumber:
        # Division using the conjugate approach
        if not isinstance(other, NeutrosophicBicomplexNumber):
            return NotImplemented
        
        # Compute conjugate (C - DI)
        conjugate = NeutrosophicBicomplexNumber(other.determinate, -other.indeterminate)
        
        # Multiply numerator and denominator by conjugate
        numerator = self * conjugate
        denominator = other * conjugate
        
        # Denominator should be a bicomplex number (only determinate part)
        if abs(denominator.indeterminate.z1.real) > 1e-10 or abs(denominator.indeterminate.z1.imag) > 1e-10 or \
           abs(denominator.indeterminate.z2.real) > 1e-10 or abs(denominator.indeterminate.z2.imag) > 1e-10:
            raise ValueError("Division resulted in non-bicomplex denominator")
            
        return NeutrosophicBicomplexNumber(numerator.determinate / denominator.determinate, 
                                          numerator.indeterminate / denominator.determinate)

    def __eq__(self, other) -> bool:
        if not isinstance(other, NeutrosophicBicomplexNumber):
            return NotImplemented
        return self.determinate == other.determinate and self.indeterminate == other.indeterminate

    def __repr__(self) -> str:
        return f"({self.determinate}) + ({self.indeterminate})I"


@dataclass(frozen=True)
class HyperrealNumber(AdvancedNumber):
    """
    Represents a hyperreal number as a sequence of real numbers.
    Note: This is a conceptual implementation. A full implementation requires
    a non-principal ultrafilter, which is non-constructive.
    """
    sequence_func: callable

    def __post_init__(self):
        if not callable(self.sequence_func):
            raise TypeError("sequence_func must be a callable function.")

    def __add__(self, other: HyperrealNumber) -> HyperrealNumber:
        if not isinstance(other, HyperrealNumber):
            return NotImplemented
        return HyperrealNumber(lambda n: self.sequence_func(n) + other.sequence_func(n))

    def __sub__(self, other: HyperrealNumber) -> HyperrealNumber:
        if not isinstance(other, HyperrealNumber):
            return NotImplemented
        return HyperrealNumber(lambda n: self.sequence_func(n) - other.sequence_func(n))

    def __mul__(self, other: HyperrealNumber) -> HyperrealNumber:
        if not isinstance(other, HyperrealNumber):
            return NotImplemented
        return HyperrealNumber(lambda n: self.sequence_func(n) * other.sequence_func(n))

    def __truediv__(self, other: HyperrealNumber) -> HyperrealNumber:
        # Avoid division by zero in the sequence
        def div_func(n):
            denominator = other.sequence_func(n)
            if abs(denominator) < 1e-10:
                # This case needs a more rigorous definition based on the ultrafilter.
                # For simplicity, we return 0, but this is not generally correct.
                return 0
            return self.sequence_func(n) / denominator
        return HyperrealNumber(div_func)

    def __eq__(self, other) -> bool:
        # Equality for hyperreals means the set of indices where sequences are equal
        # belongs to the ultrafilter. This cannot be implemented directly.
        raise NotImplementedError("Equality for hyperreal numbers cannot be determined constructively.")

    def __repr__(self) -> str:
        return f"Hyperreal(sequence: {self.sequence_func(1)}, {self.sequence_func(2)}, ...)"

# =============================================
# Cayley-Dickson Construction Wrapper
# =============================================

def generate_cayley_dickson_number(dimension: int, *components: float) -> Any:
    """
    Generates a hypercomplex number using the Cayley-Dickson construction.
    Args:
        dimension: The dimension of the hypercomplex number (2^n)
        *components: The components of the number
    Returns:
        A hypercomplex number of the specified dimension
    """
    if dimension not in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
        raise ValueError("Dimension must be a power of 2 up to 256")
    
    if len(components) != dimension:
        raise ValueError(f"Expected {dimension} components, got {len(components)}")
    
    # Map dimension to the appropriate hypercomplex class
    dimension_map = {
        1: reals,
        2: Complex,
        4: Quaternion,
        8: Octonion,
        16: Sedenion,
        32: Pathion,
        64: Chingon,
        128: Routon,
        256: Voudon
    }
    
    return dimension_map[dimension](*components)

# =============================================
# Cayley-Dickson Construction Helper
# =============================================

def generate_cd_chain(max_level: int = 8) -> List:
    """
    Generates a chain of Cayley-Dickson algebras up to the specified level.
    Args:
        max_level: Maximum level of the Cayley-Dickson construction
    Returns:
        List of hypercomplex number types [CD0, CD1, CD2, ..., CD_max_level]
    """
    CD = [reals()]  # CD0 = Real numbers
    
    for i in range(max_level):
        CD.append(cayley_dickson_construction(CD[-1]))
    
    return CD


# =============================================
# Helper Functions
# =============================================

def oresme_sequence(n_terms: int) -> List[float]:
    """Generates the first n terms of the Oresme sequence (n / 2^n)."""
    if n_terms <= 0:
        return []
    return [n / (2 ** n) for n in range(1, n_terms + 1)]


def harmonic_numbers(n_terms: int) -> Generator[Fraction, None, None]:
    """
    Generates the first n harmonic numbers (H_n = 1 + 1/2 + ... + 1/n)
    as exact fractions.
    """
    if n_terms <= 0:
        return
    current_sum = Fraction(0)
    for i in range(1, n_terms + 1):
        current_sum += Fraction(1, i)
        yield current_sum


def binet_formula(n: int) -> float:
    """Calculates the nth Fibonacci number using Binet's formula."""
    if n < 0:
        raise ValueError("The Fibonacci sequence is not defined for negative integers.")
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    return (phi**n - (1 - phi)**n) / sqrt5

# =============================================
# Example Usage
# =============================================

if __name__ == "__main__":
    # Generate Cayley-Dickson chain
    CD = generate_cd_chain(8)  # Up to 256 dimensions (CD0 to CD8)
    
    # CD chain mapping:
    # CD[0] = Real numbers (1 dimension)
    # CD[1] = Complex numbers (2 dimensions)
    # CD[2] = Quaternions (4 dimensions)
    # CD[3] = Octonions (8 dimensions)
    # CD[4] = Sedenions (16 dimensions)
    # CD[5] = Pathions (32 dimensions)
    # CD[6] = Chingons (64 dimensions)
    # CD[7] = Routons (128 dimensions)
    # CD[8] = Voudons (256 dimensions)
    
    # Generate an octonion (8 dimensions)
    octonion = CD[3](1, 0, 2, 0, 3)  # Missing components auto-filled with zeros
    print(f"Octonion: {octonion}")  # -> (1 0 2 0 3 0 0 0)
    
    # Generate other types
    complex_num = CD[1](1, 2)  # Complex number
    quaternion = CD[2](1, 2, 3, 4)  # Quaternion
    sedenion = CD[4](*range(1, 17))  # Sedenion with values 1-16
    
    print(f"Complex: {complex_num}")
    print(f"Quaternion: {quaternion}")
    print(f"Sedenion: {sedenion}")
    
    # Or use the predefined types directly
    octonion2 = Octonion(1, 0, 2, 0, 3)
    print(f"Octonion (predefined): {octonion2}")
    
    # Bicomplex number example
    bc1 = BicomplexNumber(Complex(1, 2), Complex(3, 4))
    bc2 = BicomplexNumber(Complex(5, 6), Complex(7, 8))
    print(f"Bicomplex multiplication: {bc1} * {bc2} = {bc1 * bc2}")


    # Example usage of hypercomplex numbers
    c1 = Complex(1, 2)
    c2 = Complex(3, 4)
    print(f"Complex numbers: {c1} + {c2} = {c1 + c2}")
    
    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(5, 6, 7, 8)
    print(f"Quaternions: {q1} * {q2} = {q1 * q2}")
    
    
    # Generate higher dimension numbers using cayley_dickson_algebra
    octonion_type = cayley_dickson_algebra(3)  # 2^3 = 8 dimensions
    octonion = octonion_type(1, 2, 3, 4, 5, 6, 7, 8)
    print(f"Octonion: {octonion}")
    
    # Or use the predefined types
    sedenion = Sedenion(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    print(f"Sedenion: {sedenion}") # 2^4 = 16 dimensions

    pathion = Pathion(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32)
    print(f"Pathion: {pathion}") # 2^5 = 32 dimensions

    Real=reals()
    print(Real(4))               # -> (4)
    C = cayley_dickson_construction(Complex)
    print(C(3-7j))               # -> (3 -7)
    CD4 = cayley_dickson_construction(CD[1])
    print(CD4(.1, -2.2, 3.3e3))  # -> (0.1 -2.2 3300 0)
    CD[3] = cayley_dickson_construction(CD[2])
    print(CD[3](1, 0, 2, 0, 3))  # -> (1 0 2 0 3 0 0 0)
