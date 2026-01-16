"""
adnus (AdNuS): A Python library for Advanced Number Systems.
Unified interface for hypercomplex numbers, neutrosophic numbers, and other advanced number systems.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from fractions import Fraction
import math
from math import sqrt
from typing import List, Union, Generator, Tuple, Any, Optional
import numpy as np
import warnings

# Try to import kececinumbers, but provide fallbacks
try:
    from kececinumbers import (
        reals, Complex as KComplex, Quaternion as KQuaternion, 
        Octonion as KOctonion, Sedenion as KSedenion,
        Pathion as KPathion, Chingon as KChingon, 
        Routon as KRouton, Voudon as KVoudon,
        cayley_dickson_process, cayley_dickson_cebir
    )
    HAS_KECECI = True
except ImportError:
    HAS_KECECI = False
    # generate dummy classes for type hints
    class KComplex: pass
    class KQuaternion: pass
    class KOctonion: pass
    class KSedenion: pass
    class KPathion: pass
    class KChingon: pass
    class KRouton: pass
    class KVoudon: pass


# =============================================
# Abstract Base Class
# =============================================

class AdvancedNumber(ABC):
    """Abstract Base Class for all advanced number systems."""
    
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
    
    @abstractmethod
    def norm(self) -> float:
        """Return the Euclidean norm/magnitude."""
        pass
    
    @abstractmethod
    def conjugate(self):
        """Return the conjugate."""
        pass
    
    @abstractmethod
    def to_hypercomplex(self) -> 'HypercomplexNumber':
        """Convert to HypercomplexNumber."""
        pass

# =============================================
# Complex Number Implementation
# =============================================

class ComplexNumber(AdvancedNumber):
    """Complex number implementation."""
    
    def __init__(self, real: float, imag: float = 0.0):
        self._real = float(real)
        self._imag = float(imag)
    
    @property
    def real(self) -> float:
        return self._real
    
    @property
    def imag(self) -> float:
        return self._imag
    
    def __add__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.real + other.real, self.imag + other.imag)
        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real + float(other), self.imag)
        elif isinstance(other, complex):
            return ComplexNumber(self.real + other.real, self.imag + other.imag)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.real - other.real, self.imag - other.imag)
        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real - float(other), self.imag)
        elif isinstance(other, complex):
            return ComplexNumber(self.real - other.real, self.imag - other.imag)
        return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return ComplexNumber(float(other) - self.real, -self.imag)
        elif isinstance(other, complex):
            return ComplexNumber(other.real - self.real, other.imag - self.imag)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, ComplexNumber):
            real = self.real * other.real - self.imag * other.imag
            imag = self.real * other.imag + self.imag * other.real
            return ComplexNumber(real, imag)
        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real * float(other), self.imag * float(other))
        elif isinstance(other, complex):
            return self * ComplexNumber(other.real, other.imag)
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, ComplexNumber):
            denominator = other.norm() ** 2
            if denominator == 0:
                raise ZeroDivisionError("Division by zero")
            conj = other.conjugate()
            result = self * conj
            return ComplexNumber(result.real / denominator, result.imag / denominator)
        elif isinstance(other, (int, float)):
            if float(other) == 0:
                raise ZeroDivisionError("Division by zero")
            return ComplexNumber(self.real / float(other), self.imag / float(other))
        elif isinstance(other, complex):
            return self / ComplexNumber(other.real, other.imag)
        return NotImplemented
    
    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return ComplexNumber(float(other), 0) / self
        elif isinstance(other, complex):
            return ComplexNumber(other.real, other.imag) / self
        return NotImplemented
    
    def __neg__(self):
        return ComplexNumber(-self.real, -self.imag)
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        return self.norm()
    
    def __eq__(self, other):
        if isinstance(other, ComplexNumber):
            return math.isclose(self.real, other.real) and math.isclose(self.imag, other.imag)
        elif isinstance(other, (int, float)):
            return math.isclose(self.real, float(other)) and math.isclose(self.imag, 0)
        elif isinstance(other, complex):
            return math.isclose(self.real, other.real) and math.isclose(self.imag, other.imag)
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((round(self.real, 12), round(self.imag, 12)))
    
    def __repr__(self):
        return f"ComplexNumber({self.real}, {self.imag})"
    
    def __str__(self):
        if self.imag >= 0:
            return f"{self.real} + {self.imag}i"
        else:
            return f"{self.real} - {-self.imag}i"
    
    def norm(self) -> float:
        return math.sqrt(self.real**2 + self.imag**2)
    
    def conjugate(self):
        return ComplexNumber(self.real, -self.imag)
    
    def to_complex(self) -> complex:
        return complex(self.real, self.imag)

# =============================================
# Bicomplex Number (uses HypercomplexNumber for components)
# =============================================

@dataclass(frozen=True)
class BicomplexNumber(AdvancedNumber):
    """
    Bicomplex number: z = z1 + z2·j where z1, z2 ∈ ℂ and j² = -1 (independent imaginary unit).
    """
    z1: HypercomplexNumber  # First complex component
    z2: HypercomplexNumber  # Second complex component
    
    def __post_init__(self):
        # Convert to HypercomplexNumber if needed
        # DÜZELTME: Eğer z1 veya z2 HypercomplexNumber değilse, dönüştür
        if not isinstance(self.z1, HypercomplexNumber):
            if isinstance(self.z1, complex):
                object.__setattr__(self, 'z1', HypercomplexNumber(self.z1.real, self.z1.imag, dimension=2))
            elif isinstance(self.z1, (int, float)):
                object.__setattr__(self, 'z1', HypercomplexNumber(float(self.z1), 0.0, dimension=2))
            elif isinstance(self.z1, ComplexNumber):  # Eğer ComplexNumber sınıfı varsa
                object.__setattr__(self, 'z1', HypercomplexNumber(self.z1.real, self.z1.imag, dimension=2))
            else:
                # Diğer türler için from_any kullan
                object.__setattr__(self, 'z1', HypercomplexNumber.from_any(self.z1).pad_to_dimension(2))
        
        if not isinstance(self.z2, HypercomplexNumber):
            if isinstance(self.z2, complex):
                object.__setattr__(self, 'z2', HypercomplexNumber(self.z2.real, self.z2.imag, dimension=2))
            elif isinstance(self.z2, (int, float)):
                object.__setattr__(self, 'z2', HypercomplexNumber(float(self.z2), 0.0, dimension=2))
            elif isinstance(self.z2, ComplexNumber):  # Eğer ComplexNumber sınıfı varsa
                object.__setattr__(self, 'z2', HypercomplexNumber(self.z2.real, self.z2.imag, dimension=2))
            else:
                # Diğer türler için from_any kullan
                object.__setattr__(self, 'z2', HypercomplexNumber.from_any(self.z2).pad_to_dimension(2))
        
        # Ensure both are complex numbers (dimension 2)
        # DÜZELTME: dimension attribute kontrolü
        if hasattr(self.z1, 'dimension') and self.z1.dimension != 2:
            object.__setattr__(self, 'z1', self.z1.pad_to_dimension(2))
        
        if hasattr(self.z2, 'dimension') and self.z2.dimension != 2:
            object.__setattr__(self, 'z2', self.z2.pad_to_dimension(2))
    
    def __add__(self, other):
        if isinstance(other, BicomplexNumber):
            return BicomplexNumber(self.z1 + other.z1, self.z2 + other.z2)
        else:
            # Try to convert to HypercomplexNumber first
            try:
                other_h = HypercomplexNumber.from_any(other)
                if other_h.dimension == 2:
                    return BicomplexNumber(self.z1 + other_h, self.z2)
                else:
                    # If higher dimension, convert to HypercomplexNumber
                    return self.to_hypercomplex() + other_h
            except:
                return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, BicomplexNumber):
            return BicomplexNumber(self.z1 - other.z1, self.z2 - other.z2)
        else:
            try:
                other_h = HypercomplexNumber.from_any(other)
                if other_h.dimension == 2:
                    return BicomplexNumber(self.z1 - other_h, self.z2)
                else:
                    return self.to_hypercomplex() - other_h
            except:
                return NotImplemented
    
    def __rsub__(self, other):
        try:
            other_h = HypercomplexNumber.from_any(other)
            if other_h.dimension == 2:
                return BicomplexNumber(other_h - self.z1, -self.z2)
            else:
                return other_h - self.to_hypercomplex()
        except:
            return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, BicomplexNumber):
            # (z1 + z2j)(w1 + w2j) = (z1w1 - z2w2) + (z1w2 + z2w1)j
            z1w1 = self.z1 * other.z1
            z2w2 = self.z2 * other.z2
            z1w2 = self.z1 * other.z2
            z2w1 = self.z2 * other.z1
            
            return BicomplexNumber(z1w1 - z2w2, z1w2 + z2w1)
        else:
            try:
                other_h = HypercomplexNumber.from_any(other)
                if other_h.dimension == 2:
                    return BicomplexNumber(self.z1 * other_h, self.z2 * other_h)
                else:
                    return self.to_hypercomplex() * other_h
            except:
                return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, BicomplexNumber):
            # Use conjugate method: a/b = a * conj(b) / |b|²
            conj = other.conjugate()
            numerator = self * conj
            denominator = other.norm() ** 2
            if denominator == 0:
                raise ZeroDivisionError("Division by zero bicomplex")
            return BicomplexNumber(numerator.z1 / denominator, numerator.z2 / denominator)
        else:
            try:
                other_h = HypercomplexNumber.from_any(other)
                if other == 0:
                    raise ZeroDivisionError("Division by zero")
                return BicomplexNumber(self.z1 / other_h, self.z2 / other_h)
            except:
                return NotImplemented
    
    def __rtruediv__(self, other):
        try:
            other_h = HypercomplexNumber.from_any(other)
            if other_h.dimension == 2:
                return BicomplexNumber(other_h, HypercomplexNumber(0, 0, dimension=2)) / self
            else:
                return other_h / self.to_hypercomplex()
        except:
            return NotImplemented
    
    def __neg__(self):
        return BicomplexNumber(-self.z1, -self.z2)
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        return self.norm()
    
    def __eq__(self, other):
        if isinstance(other, BicomplexNumber):
            return self.z1 == other.z1 and self.z2 == other.z2
        else:
            try:
                other_h = HypercomplexNumber.from_any(other)
                if other_h.dimension == 2:
                    return self.z1 == other_h and self.z2 == HypercomplexNumber(0, 0, dimension=2)
                else:
                    return self.to_hypercomplex() == other_h
            except:
                return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.z1, self.z2))
    
    def __repr__(self):
        return f"BicomplexNumber(z1={self.z1}, z2={self.z2})"
    
    def __str__(self):
        return f"({self.z1}) + ({self.z2})·j"
    
    def norm(self) -> float:
        return math.sqrt(self.z1.norm()**2 + self.z2.norm()**2)
    
    def conjugate(self):
        return BicomplexNumber(self.z1.conjugate(), -self.z2)
    
    def components(self) -> Tuple[float, float, float, float]:
        """Return (Re(z1), Im(z1), Re(z2), Im(z2))."""
        return (self.z1[0], self.z1[1], self.z2[0], self.z2[1])
    
    def to_hypercomplex(self) -> HypercomplexNumber:
        """Convert to 4D HypercomplexNumber."""
        return HypercomplexNumber(
            self.z1[0], self.z1[1], 
            self.z2[0], self.z2[1],
            dimension=4
        )



# =============================================
# Neutrosophic Number
# =============================================

@dataclass(frozen=True)
class NeutrosophicNumber(AdvancedNumber):
    """
    Neutrosophic number: a + bI where I² = I (indeterminacy).
    """
    determinate: float
    indeterminate: float
    
    def __add__(self, other):
        if isinstance(other, NeutrosophicNumber):
            return NeutrosophicNumber(
                self.determinate + other.determinate,
                self.indeterminate + other.indeterminate
            )
        elif isinstance(other, (int, float)):
            return NeutrosophicNumber(self.determinate + other, self.indeterminate)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, NeutrosophicNumber):
            return NeutrosophicNumber(
                self.determinate - other.determinate,
                self.indeterminate - other.indeterminate
            )
        elif isinstance(other, (int, float)):
            return NeutrosophicNumber(self.determinate - other, self.indeterminate)
        return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return NeutrosophicNumber(other - self.determinate, -self.indeterminate)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, NeutrosophicNumber):
            # (a + bI)(c + dI) = ac + (ad + bc + bd)I
            determinate = self.determinate * other.determinate
            indeterminate = (self.determinate * other.indeterminate +
                           self.indeterminate * other.determinate +
                           self.indeterminate * other.indeterminate)
            return NeutrosophicNumber(determinate, indeterminate)
        elif isinstance(other, (int, float)):
            return NeutrosophicNumber(
                self.determinate * other,
                self.indeterminate * other
            )
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero")
            return NeutrosophicNumber(
                self.determinate / other,
                self.indeterminate / other
            )
        elif isinstance(other, NeutrosophicNumber):
            # Use conjugate: (a + bI)/(c + dI) = (a + bI)(c - dI) / (c² + (c-d)d)
            conj = other.conjugate()
            numerator = self * conj
            denominator = other.determinate**2 + (other.determinate - other.indeterminate) * other.indeterminate
            if denominator == 0:
                raise ZeroDivisionError("Division by zero neutrosophic")
            return NeutrosophicNumber(
                numerator.determinate / denominator,
                numerator.indeterminate / denominator
            )
        return NotImplemented
    
    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return NeutrosophicNumber(other, 0) / self
        return NotImplemented
    
    def __neg__(self):
        return NeutrosophicNumber(-self.determinate, -self.indeterminate)
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        return self.norm()
    
    def __eq__(self, other):
        if isinstance(other, NeutrosophicNumber):
            return (math.isclose(self.determinate, other.determinate) and
                    math.isclose(self.indeterminate, other.indeterminate))
        elif isinstance(other, (int, float)):
            return math.isclose(self.determinate, other) and math.isclose(self.indeterminate, 0)
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((round(self.determinate, 12), round(self.indeterminate, 12)))
    
    def __repr__(self):
        return f"NeutrosophicNumber({self.determinate}, {self.indeterminate})"
    
    def __str__(self):
        if self.indeterminate >= 0:
            return f"{self.determinate} + {self.indeterminate}I"
        else:
            return f"{self.determinate} - {-self.indeterminate}I"
    
    def norm(self) -> float:
        return math.sqrt(self.determinate**2 + self.indeterminate**2)
    
    def conjugate(self):
        return NeutrosophicNumber(self.determinate, -self.indeterminate)

# =============================================
# Unified Number System: HypercomplexNumber
# =============================================

class HypercomplexNumber(AdvancedNumber):
    """
    Unified hypercomplex number implementation for all dimensions.
    Supports: Real (1), Complex (2), Quaternion (4), Octonion (8), etc.
    """
    
    # Dimension names
    DIM_NAMES = {
        1: "Real",
        2: "Complex",
        4: "Quaternion",
        8: "Octonion",
        16: "Sedenion",
        32: "Pathion",
        64: "Chingon",
        128: "Routon",
        256: "Voudon"
    }
    
    def __init__(self, *components: float, dimension: Optional[int] = None):
        """
        Initialize hypercomplex number.
        
        Args:
            *components: Number components
            dimension: Dimension (power of 2). If None, inferred from components.
        """
        if dimension is None:
            # Find smallest power of 2 >= len(components)
            n = len(components)
            dimension = 1
            while dimension < n and dimension < 256:
                dimension <<= 1
        
        if dimension & (dimension - 1) != 0 or dimension < 1:
            raise ValueError(f"Dimension must be power of 2 (1-256), got {dimension}")
        
        self.dimension = dimension
        
        # Pad or truncate components
        if len(components) < dimension:
            self.coeffs = list(components) + [0.0] * (dimension - len(components))
        elif len(components) > dimension:
            self.coeffs = components[:dimension]
        else:
            self.coeffs = list(components)
        
        # Type name - DÜZELTİLDİ: 'dim' yerine 'dimension' kullan
        self.type_name = self.DIM_NAMES.get(dimension, f"Hypercomplex{dimension}")
    
    @classmethod
    def from_real(cls, value: float) -> 'HypercomplexNumber':
        """Create from a real number."""
        return cls(value, dimension=1)
    
    @classmethod
    def from_complex(cls, real: float, imag: float) -> 'HypercomplexNumber':
        """Create from complex components."""
        return cls(real, imag, dimension=2)
    
    @classmethod
    def from_quaternion(cls, w: float, x: float, y: float, z: float) -> 'HypercomplexNumber':
        """Create from quaternion components."""
        return cls(w, x, y, z, dimension=4)
    
    @classmethod
    def from_octonion(cls, *coeffs: float) -> 'HypercomplexNumber':
        """Create from octonion components."""
        if len(coeffs) != 8:
            coeffs = list(coeffs) + [0.0] * (8 - len(coeffs))
        return cls(*coeffs, dimension=8)
    
    @classmethod
    def from_any(cls, value: Any) -> 'HypercomplexNumber':
        """Create from any numeric type."""
        if isinstance(value, HypercomplexNumber):
            return value
        elif isinstance(value, (int, float)):
            return cls.from_real(float(value))
        elif isinstance(value, complex):
            return cls.from_complex(value.real, value.imag)
        elif isinstance(value, (list, tuple)):
            return cls(*value)
        else:
            try:
                return cls.from_real(float(value))
            except:
                raise ValueError(f"Cannot convert {type(value)} to HypercomplexNumber")
    
    @property
    def real(self) -> float:
        """Real part (first component)."""
        return self.coeffs[0]
    
    @property
    def imag(self) -> float:
        """Imaginary part (for complex numbers)."""
        if self.dimension >= 2:
            return self.coeffs[1]
        return 0.0
    
    def __len__(self):
        return self.dimension
    
    def __getitem__(self, idx):
        return self.coeffs[idx]
    
    def __iter__(self):
        return iter(self.coeffs)
    
    def __add__(self, other):
        # Convert other to HypercomplexNumber if needed
        if not isinstance(other, HypercomplexNumber):
            try:
                other = self.from_any(other)
            except:
                return NotImplemented
        
        # Handle different dimensions
        if self.dimension != other.dimension:
            common_dim = max(self.dimension, other.dimension)
            self_padded = self.pad_to_dimension(common_dim)
            other_padded = other.pad_to_dimension(common_dim)
            return self_padded + other_padded
        
        new_coeffs = [a + b for a, b in zip(self.coeffs, other.coeffs)]
        return HypercomplexNumber(*new_coeffs, dimension=self.dimension)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        # Convert other to HypercomplexNumber if needed
        if not isinstance(other, HypercomplexNumber):
            try:
                other = self.from_any(other)
            except:
                return NotImplemented
        
        # Handle different dimensions
        if self.dimension != other.dimension:
            common_dim = max(self.dimension, other.dimension)
            self_padded = self.pad_to_dimension(common_dim)
            other_padded = other.pad_to_dimension(common_dim)
            return self_padded - other_padded
        
        new_coeffs = [a - b for a, b in zip(self.coeffs, other.coeffs)]
        return HypercomplexNumber(*new_coeffs, dimension=self.dimension)
    
    def __rsub__(self, other):
        # Convert other to HypercomplexNumber
        try:
            other_num = self.from_any(other)
            return other_num - self
        except:
            return NotImplemented
    
    def _multiply_complex(self, other: 'HypercomplexNumber') -> 'HypercomplexNumber':
        """Complex multiplication (dimension 2)."""
        a, b = self.coeffs
        c, d = other.coeffs
        real = a*c - b*d
        imag = a*d + b*c
        return HypercomplexNumber(real, imag, dimension=2)
    
    def _multiply_quaternion(self, other: 'HypercomplexNumber') -> 'HypercomplexNumber':
        """Quaternion multiplication (dimension 4)."""
        w1, x1, y1, z1 = self.coeffs
        w2, x2, y2, z2 = other.coeffs
        
        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2
        
        return HypercomplexNumber(w, x, y, z, dimension=4)
    
    def __mul__(self, other):
        # Convert other to HypercomplexNumber if needed
        if not isinstance(other, HypercomplexNumber):
            try:
                other = self.from_any(other)
            except:
                return NotImplemented
        
        # Handle different dimensions
        if self.dimension != other.dimension:
            common_dim = max(self.dimension, other.dimension)
            self_padded = self.pad_to_dimension(common_dim)
            other_padded = other.pad_to_dimension(common_dim)
            return self_padded * other_padded
        
        # Different multiplication rules based on dimension
        if self.dimension == 1:
            # Real multiplication
            return HypercomplexNumber(self.coeffs[0] * other.coeffs[0], dimension=1)
        
        elif self.dimension == 2:
            # Complex multiplication
            return self._multiply_complex(other)
        
        elif self.dimension == 4:
            # Quaternion multiplication
            return self._multiply_quaternion(other)
        
        else:
            # For higher dimensions, use component-wise as fallback
            warnings.warn(f"Using component-wise multiplication for {self.type_name}", RuntimeWarning)
            new_coeffs = [a * b for a, b in zip(self.coeffs, other.coeffs)]
            return HypercomplexNumber(*new_coeffs, dimension=self.dimension)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        # Convert other to HypercomplexNumber if needed
        if not isinstance(other, HypercomplexNumber):
            try:
                other = self.from_any(other)
            except:
                return NotImplemented
        
        # Use inverse for division
        return self * other.inverse()
    
    def __rtruediv__(self, other):
        # Convert other to HypercomplexNumber
        try:
            other_num = self.from_any(other)
            return other_num / self
        except:
            return NotImplemented
    
    def __neg__(self):
        new_coeffs = [-c for c in self.coeffs]
        return HypercomplexNumber(*new_coeffs, dimension=self.dimension)
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        return self.norm()
    
    def __eq__(self, other):
        if not isinstance(other, HypercomplexNumber):
            try:
                other = self.from_any(other)
            except:
                return False
        
        if self.dimension != other.dimension:
            return False
        
        return all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(self.coeffs, other.coeffs))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(tuple(round(c, 12) for c in self.coeffs))
    
    def __repr__(self):
        return f"HypercomplexNumber({', '.join(map(str, self.coeffs))}, dimension={self.dimension})"
    
    def __str__(self):
        if self.dimension == 1:
            return f"{self.type_name}({self.coeffs[0]})"
        elif self.dimension == 2:
            a, b = self.coeffs
            if b >= 0:
                return f"{self.type_name}({a} + {b}i)"
            else:
                return f"{self.type_name}({a} - {-b}i)"
        elif self.dimension <= 8:
            non_zero = [(i, c) for i, c in enumerate(self.coeffs) if abs(c) > 1e-10]
            if not non_zero:
                return f"{self.type_name}(0)"
            
            parts = []
            for i, c in non_zero:
                if i == 0:
                    parts.append(f"{c:.4f}")
                else:
                    sign = "+" if c >= 0 else "-"
                    parts.append(f"{sign} {abs(c):.4f}e{i}")
            return f"{self.type_name}({' '.join(parts)})"
        else:
            return f"{self.type_name}[real={self.real:.4f}, norm={self.norm():.4f}, dim={self.dimension}]"
    
    def norm(self) -> float:
        """Euclidean norm."""
        return math.sqrt(sum(c**2 for c in self.coeffs))
    
    def conjugate(self):
        """Conjugate (negate all imaginary parts)."""
        if self.dimension == 1:
            return self
        
        new_coeffs = self.coeffs.copy()
        for i in range(1, self.dimension):
            new_coeffs[i] = -new_coeffs[i]
        
        return HypercomplexNumber(*new_coeffs, dimension=self.dimension)
    
    def inverse(self):
        """Multiplicative inverse."""
        norm_sq = self.norm() ** 2
        if norm_sq == 0:
            raise ZeroDivisionError("Cannot invert zero element")
        
        conj = self.conjugate()
        new_coeffs = [c / norm_sq for c in conj.coeffs]
        return HypercomplexNumber(*new_coeffs, dimension=self.dimension)
    
    def pad_to_dimension(self, new_dim: int) -> 'HypercomplexNumber':
        """Pad to higher dimension with zeros."""
        if new_dim < self.dimension:
            raise ValueError(f"Cannot pad to smaller dimension: {new_dim} < {self.dimension}")
        
        if new_dim == self.dimension:
            return self
        
        new_coeffs = self.coeffs + [0.0] * (new_dim - self.dimension)
        return HypercomplexNumber(*new_coeffs, dimension=new_dim)
    
    def truncate_to_dimension(self, new_dim: int) -> 'HypercomplexNumber':
        """Truncate to smaller dimension."""
        if new_dim > self.dimension:
            raise ValueError(f"Cannot truncate to larger dimension: {new_dim} > {self.dimension}")
        
        if new_dim == self.dimension:
            return self
        
        new_coeffs = self.coeffs[:new_dim]
        return HypercomplexNumber(*new_coeffs, dimension=new_dim)
    
    def to_list(self) -> List[float]:
        """Convert to Python list."""
        return self.coeffs.copy()
    
    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array(self.coeffs, dtype=np.float64)
    
    def copy(self) -> 'HypercomplexNumber':
        """Generate a copy."""
        return HypercomplexNumber(*self.coeffs, dimension=self.dimension)
    
    def __float__(self):
        """Convert to float (returns real part)."""
        return float(self.real)
    
    def to_complex(self) -> complex:
        """Convert to Python complex if possible."""
        if self.dimension >= 2:
            return complex(self.coeffs[0], self.coeffs[1])
        return complex(self.coeffs[0], 0.0)
    
    def to_hypercomplex(self) -> 'HypercomplexNumber':
        """Convert to HypercomplexNumber (identity for this class)."""
        return self

# =============================================
# Neutrosophic Number
# =============================================

@dataclass(frozen=True)
class NeutrosophicNumber(AdvancedNumber):
    """
    Neutrosophic number: a + bI where I² = I (indeterminacy).
    """
    determinate: float
    indeterminate: float
    
    def __add__(self, other):
        if isinstance(other, NeutrosophicNumber):
            return NeutrosophicNumber(
                self.determinate + other.determinate,
                self.indeterminate + other.indeterminate
            )
        elif isinstance(other, (int, float)):
            return NeutrosophicNumber(self.determinate + other, self.indeterminate)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, NeutrosophicNumber):
            return NeutrosophicNumber(
                self.determinate - other.determinate,
                self.indeterminate - other.indeterminate
            )
        elif isinstance(other, (int, float)):
            return NeutrosophicNumber(self.determinate - other, self.indeterminate)
        return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return NeutrosophicNumber(other - self.determinate, -self.indeterminate)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, NeutrosophicNumber):
            # (a + bI)(c + dI) = ac + (ad + bc + bd)I
            determinate = self.determinate * other.determinate
            indeterminate = (self.determinate * other.indeterminate +
                           self.indeterminate * other.determinate +
                           self.indeterminate * other.indeterminate)
            return NeutrosophicNumber(determinate, indeterminate)
        elif isinstance(other, (int, float)):
            return NeutrosophicNumber(
                self.determinate * other,
                self.indeterminate * other
            )
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero")
            return NeutrosophicNumber(
                self.determinate / other,
                self.indeterminate / other
            )
        elif isinstance(other, NeutrosophicNumber):
            # Use conjugate: (a + bI)/(c + dI) = (a + bI)(c - dI) / (c² + (c-d)d)
            conj = other.conjugate()
            numerator = self * conj
            denominator = other.determinate**2 + (other.determinate - other.indeterminate) * other.indeterminate
            if denominator == 0:
                raise ZeroDivisionError("Division by zero neutrosophic")
            return NeutrosophicNumber(
                numerator.determinate / denominator,
                numerator.indeterminate / denominator
            )
        return NotImplemented
    
    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return NeutrosophicNumber(other, 0) / self
        return NotImplemented
    
    def __neg__(self):
        return NeutrosophicNumber(-self.determinate, -self.indeterminate)
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        return self.norm()
    
    def __eq__(self, other):
        if isinstance(other, NeutrosophicNumber):
            return (math.isclose(self.determinate, other.determinate) and
                    math.isclose(self.indeterminate, other.indeterminate))
        elif isinstance(other, (int, float)):
            return math.isclose(self.determinate, other) and math.isclose(self.indeterminate, 0)
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((round(self.determinate, 12), round(self.indeterminate, 12)))
    
    def __repr__(self):
        return f"NeutrosophicNumber({self.determinate}, {self.indeterminate})"
    
    def __str__(self):
        if self.indeterminate >= 0:
            return f"{self.determinate} + {self.indeterminate}I"
        else:
            return f"{self.determinate} - {-self.indeterminate}I"
    
    def norm(self) -> float:
        return math.sqrt(self.determinate**2 + self.indeterminate**2)
    
    def conjugate(self):
        return NeutrosophicNumber(self.determinate, -self.indeterminate)
    
    def to_hypercomplex(self) -> HypercomplexNumber:
        """Convert to 2D HypercomplexNumber (treats I as imaginary unit)."""
        return HypercomplexNumber(self.determinate, self.indeterminate, dimension=2)


# =============================================
# Factory Functions (Simplified)
# =============================================

def Real(x: float) -> HypercomplexNumber:
    """Generate a real number (1D hypercomplex)."""
    return HypercomplexNumber.from_real(x)

def Complex(real: float, imag: float) -> HypercomplexNumber:
    """Generate a complex number (2D hypercomplex)."""
    return HypercomplexNumber.from_complex(real, imag)

def Quaternion(w: float, x: float, y: float, z: float) -> HypercomplexNumber:
    """Generate a quaternion (4D hypercomplex)."""
    return HypercomplexNumber.from_quaternion(w, x, y, z)

def Octonion(*coeffs: float) -> HypercomplexNumber:
    """Generate an octonion (8D hypercomplex)."""
    return HypercomplexNumber.from_octonion(*coeffs)

def Bicomplex(z1_real: float, z1_imag: float, z2_real: float, z2_imag: float) -> BicomplexNumber:
    """Generate a bicomplex number."""
    z1 = HypercomplexNumber(z1_real, z1_imag, dimension=2)
    z2 = HypercomplexNumber(z2_real, z2_imag, dimension=2)
    return BicomplexNumber(z1, z2)

def Neutrosophic(determinate: float, indeterminate: float) -> NeutrosophicNumber:
    """Generate a neutrosophic number."""
    return NeutrosophicNumber(determinate, indeterminate)


def Sedenion(*coeffs) -> HypercomplexNumber:
    """Generate a sedenion."""
    if len(coeffs) != 16:
        coeffs = list(coeffs) + [0.0] * (16 - len(coeffs))
    return HypercomplexNumber(*coeffs, dimension=16)

def Pathion(*coeffs) -> HypercomplexNumber:
    """Generate a pathion."""
    if len(coeffs) != 32:
        coeffs = list(coeffs) + [0.0] * (32 - len(coeffs))
    return HypercomplexNumber(*coeffs, dimension=32)

def Chingon(*coeffs) -> HypercomplexNumber:
    """Generate a chingon."""
    if len(coeffs) != 64:
        coeffs = list(coeffs) + [0.0] * (64 - len(coeffs))
    return HypercomplexNumber(*coeffs, dimension=64)

def Routon(*coeffs) -> HypercomplexNumber:
    """Generate a routon."""
    if len(coeffs) != 128:
        coeffs = list(coeffs) + [0.0] * (128 - len(coeffs))
    return HypercomplexNumber(*coeffs, dimension=128)

def Voudon(*coeffs) -> HypercomplexNumber:
    """Generate a voudon."""
    if len(coeffs) != 256:
        coeffs = list(coeffs) + [0.0] * (256 - len(coeffs))
    return HypercomplexNumber(*coeffs, dimension=256)

# =============================================
# Cayley-Dickson Implementation
# =============================================

def cayley_dickson_process(cebr: type, base_type=float) -> type:
    """
    Apply the Cayley-Dickson construction to generate an algebra of twice the dimension.
    """
    
    class CayleyDicksonCebr:
        """Hypercomplex algebra generated via Cayley-Dickson construction."""
        
        dimensions = None
        base = base_type
        
        def __init__(self, *args, pair=False):
            if pair and len(args) == 2:
                # (a, b) pair format
                self.a = self._ensure_cebr(args[0], cebr)
                self.b = self._ensure_cebr(args[1], cebr)
            else:
                # Handle various input formats
                if len(args) == 1:
                    arg = args[0]
                    # Handle complex numbers
                    if isinstance(arg, complex):
                        # Convert complex to pair (real, imag)
                        self.a = cebr(arg.real)
                        self.b = cebr(arg.imag)
                        return
                    # Handle strings
                    elif isinstance(arg, str):
                        # Try to parse as complex
                        try:
                            c = complex(arg)
                            self.a = cebr(c.real)
                            self.b = cebr(c.imag)
                            return
                        except ValueError:
                            pass
                    # Handle iterables
                    elif hasattr(arg, '__iter__'):
                        components = list(arg)
                    else:
                        components = [arg]
                else:
                    components = list(args)
                
                # Ensure even number of components
                if len(components) % 2 != 0:
                    components.append(base_type(0))
                
                half = len(components) // 2
                self.a = cebr(*components[:half])
                self.b = cebr(*components[half:])
        
        @staticmethod
        def _ensure_cebr(value, cebr_class):
            """Convert value to cebr instance if needed."""
            if isinstance(value, cebr_class):
                return value
            # Handle complex numbers
            elif isinstance(value, complex):
                return cebr_class(value.real, value.imag)
            # Handle single values
            else:
                return cebr_class(value)
        
        @classmethod
        def from_complex(cls, c: complex):
            """generate from a complex number."""
            return cls(c.real, c.imag)
        
        @classmethod
        def from_pair(cls, a, b):
            """generate from a pair (a, b)."""
            return cls(a, b, pair=True)
        
        @property
        def real(self) -> float:
            """Real part."""
            if hasattr(self.a, 'real'):
                return float(self.a.real)
            else:
                return float(self.a)
        
        def coefficients(self):
            """Get all coefficients as a tuple."""
            if hasattr(self.a, 'coefficients'):
                a_coeffs = self.a.coefficients()
            else:
                a_coeffs = (float(self.a),)
            
            if hasattr(self.b, 'coefficients'):
                b_coeffs = self.b.coefficients()
            else:
                b_coeffs = (float(self.b),)
            
            return a_coeffs + b_coeffs
        
        def __add__(self, other):
            if isinstance(other, CayleyDicksonCebr):
                return CayleyDicksonCebr(
                    self.a + other.a,
                    self.b + other.b,
                    pair=True
                )
            
            # Try to convert to this cebr
            try:
                other_cd = CayleyDicksonCebr(other)
                return self + other_cd
            except:
                return NotImplemented
        
        def __radd__(self, other):
            return self.__add__(other)
        
        def __sub__(self, other):
            if isinstance(other, CayleyDicksonCebr):
                return CayleyDicksonCebr(
                    self.a - other.a,
                    self.b - other.b,
                    pair=True
                )
            
            try:
                other_cd = CayleyDicksonCebr(other)
                return self - other_cd
            except:
                return NotImplemented
        
        def __rsub__(self, other):
            try:
                other_cd = CayleyDicksonCebr(other)
                return other_cd - self
            except:
                return NotImplemented
        
        def __mul__(self, other):
            if isinstance(other, CayleyDicksonCebr):
                # Cayley-Dickson multiplication
                a = self.a * other.a - other.b * self._conj_b()
                b = self._conj_a() * other.b + other.a * self.b
                return CayleyDicksonCebr(a, b, pair=True)
            
            # Scalar multiplication
            try:
                other_cd = CayleyDicksonCebr(other)
                return self * other_cd
            except:
                return NotImplemented
        
        def __rmul__(self, other):
            return self.__mul__(other)
        
        def __truediv__(self, other):
            if isinstance(other, CayleyDicksonCebr):
                return self * other.inverse()
            
            try:
                other_cd = CayleyDicksonCebr(other)
                return self / other_cd
            except:
                return NotImplemented
        
        def __rtruediv__(self, other):
            try:
                other_cd = CayleyDicksonCebr(other)
                return other_cd / self
            except:
                return NotImplemented
        
        def __neg__(self):
            return CayleyDicksonCebr(-self.a, -self.b, pair=True)
        
        def __pos__(self):
            return self
        
        def __abs__(self):
            return self.norm()
        
        def __eq__(self, other):
            if isinstance(other, CayleyDicksonCebr):
                return self.a == other.a and self.b == other.b
            
            try:
                other_cd = CayleyDicksonCebr(other)
                return self == other_cd
            except:
                return False
        
        def __ne__(self, other):
            return not self.__eq__(other)
        
        def __hash__(self):
            return hash((self.a, self.b))
        
        def __str__(self):
            coeffs = self.coefficients()
            if len(coeffs) <= 8:
                return f"({', '.join(f'{c:.4f}' for c in coeffs)})"
            else:
                return f"CD[{len(coeffs)}]({coeffs[0]:.4f}, ..., {coeffs[-1]:.4f})"
        
        def __repr__(self):
            return f"{self.__class__.__name__}({', '.join(map(str, self.coefficients()))})"
        
        def _conj_a(self):
            """Conjugate of a."""
            if hasattr(self.a, 'conjugate'):
                return self.a.conjugate()
            return self.a
        
        def _conj_b(self):
            """Conjugate of b."""
            if hasattr(self.b, 'conjugate'):
                return self.b.conjugate()
            return self.b
        
        def conjugate(self):
            """Conjugate: conj(a, b) = (conj(a), -b)."""
            return CayleyDicksonCebr(
                self._conj_a(),
                -self.b,
                pair=True
            )
        
        def norm(self) -> float:
            """Euclidean norm."""
            
            def get_norm_squared(x):
                if hasattr(x, 'norm_squared'):
                    return float(x.norm_squared())
                elif hasattr(x, 'norm'):
                    n = float(x.norm())
                    return n * n
                else:
                    val = float(x)
                    return val * val
            
            norm_sq = get_norm_squared(self.a) + get_norm_squared(self.b)
            return math.sqrt(norm_sq)
        
        def norm_squared(self):
            """Square of the norm."""
            def get_norm_squared(x):
                if hasattr(x, 'norm_squared'):
                    return x.norm_squared()
                elif hasattr(x, 'norm'):
                    n = x.norm()
                    return n * n
                else:
                    return x * x
            
            return get_num_squared(self.a) + get_norm_squared(self.b)
        
        def inverse(self):
            """Multiplicative inverse."""
            norm_sq = self.norm_squared()
            if float(norm_sq) == 0:
                raise ZeroDivisionError("Cannot invert zero element")
            
            conj = self.conjugate()
            return CayleyDicksonCebr(
                conj.a / norm_sq,
                conj.b / norm_sq,
                pair=True
            )
    
    # Set class attributes
    if hasattr(cebr, 'dimensions'):
        CayleyDicksonCebr.dimensions = cebr.dimensions * 2
    else:
        CayleyDicksonCebr.dimensions = 2
    
    # DÜZELTME: 'algebra_class' yerine 'cebr' kullan
    CayleyDicksonCebr.__name__ = f"CD{cebr.__name__}"
    
    return CayleyDicksonCebr


def cayley_dickson_cebr(level: int, base_type=float) -> type:
    """generate Cayley-Dickson cebr of given level."""
    if not isinstance(level, int) or level < 0:
        raise ValueError(f"Level must be non-negative integer, got {level}")
    
    # Start with real numbers
    if level == 0:
        class RealAlgebra:
            dimensions = 1
            base = base_type
            
            def __init__(self, value):
                self.value = base_type(value)
            
            def __add__(self, other):
                if isinstance(other, RealAlgebra):
                    return RealAlgebra(self.value + other.value)
                return RealAlgebra(self.value + base_type(other))
            
            def __mul__(self, other):
                if isinstance(other, RealAlgebra):
                    return RealAlgebra(self.value * other.value)
                return RealAlgebra(self.value * base_type(other))
            
            def __repr__(self):
                return f"RealAlgebra({self.value})"
            
            @property
            def real(self):
                return float(self.value)
            
            def conjugate(self):
                return self
            
            def norm(self):
                return abs(float(self.value))
        
        return RealAlgebra
    
    # Apply construction level times
    current_cebr = cayley_dickson_cebr(0, base_type)
    for i in range(level):
        current_cebr = cayley_dickson_process(current_cebr, base_type)
    
    # Set name
    if level == 0:
        current_cebr.__name__ = "Real"
    elif level == 1:
        current_cebr.__name__ = "Complex"
    elif level == 2:
        current_cebr.__name__ = "Quaternion"
    elif level == 3:
        current_cebr.__name__ = "Octonion"
    elif level == 4:
        current_cebr.__name__ = "Sedenion"
    elif level == 5:
        current_cebr.__name__ = "Pathion"
    elif level == 6:
        current_cebr.__name__ = "Chingon"
    elif level == 7:
        current_cebr.__name__ = "Routon"
    elif level == 8:
        current_cebr.__name__ = "Voudon"
    else:
        current_cebr.__name__ = f"CD{level}"
    
    return current_cebr


# =============================================
# Utility Functions
# =============================================

def generate_cd_chain(max_level: int = 8) -> list:
    """
    Generate chain of Cayley-Dickson algebras.
    
    Args:
        max_level: Maximum level to generate
    
    Returns:
        List of cebr classes
    """
    return [cayley_dickson_cebr(i) for i in range(max_level + 1)]


def cd_number_from_components(level: int, *components) -> object:
    """
    generate a Cayley-Dickson number from components.
    
    Args:
        level: cebr level
        *components: Number components
    
    Returns:
        Cayley-Dickson number instance
    """
    cebr = cayley_dickson_cebr(level)
    return cebr(*components)

def _parse_complex(s: Any) -> ComplexNumber:
    """
    Parse input as complex number.
    Supports: "1,2", "1+2j", "3j", 5, 3.14, etc.
    """
    # If already ComplexNumber
    if isinstance(s, ComplexNumber):
        return s
    
    # If complex
    if isinstance(s, complex):
        return ComplexNumber(s.real, s.imag)
    
    # If numeric
    if isinstance(s, (int, float)):
        return ComplexNumber(float(s), 0.0)
    
    # Convert to string
    if not isinstance(s, str):
        s = str(s)
    
    s = s.strip().replace(' ', '').replace('J', 'j').replace('i', 'j')
    
    # Try comma-separated
    if ',' in s:
        parts = s.split(',')
        if len(parts) == 2:
            try:
                return ComplexNumber(float(parts[0]), float(parts[1]))
            except ValueError:
                pass
    
    # Try Python's complex parser
    try:
        c = complex(s)
        return ComplexNumber(c.real, c.imag)
    except ValueError:
        pass
    
    # Try as real number
    try:
        return ComplexNumber(float(s), 0.0)
    except ValueError:
        pass
    
    # Try as pure imaginary
    if s.endswith('j'):
        try:
            imag = float(s[:-1]) if s[:-1] not in ['', '+', '-'] else 1.0
            if s.startswith('-'):
                imag = -imag
            return ComplexNumber(0.0, imag)
        except ValueError:
            pass
    
    # Fallback
    warnings.warn(f"Could not parse as complex: {repr(s)}", RuntimeWarning)
    return ComplexNumber(0.0, 0.0)


def _parse_hypercomplex(s: Any, dimension: int) -> HypercomplexNumber:
    """Parse input as hypercomplex number of given dimension."""
    try:
        # If already HypercomplexNumber
        if isinstance(s, HypercomplexNumber):
            if s.dimension == dimension:
                return s
            elif s.dimension < dimension:
                return s.pad_to_dimension(dimension)
            else:
                return s.truncate_to_dimension(dimension)
        
        # If numeric
        if isinstance(s, (int, float)):
            coeffs = [float(s)] + [0.0] * (dimension - 1)
            return HypercomplexNumber(*coeffs, dimension=dimension)
        
        # If complex
        if isinstance(s, (complex, ComplexNumber)):
            if isinstance(s, complex):
                c = s
            else:
                c = s.to_complex()
            coeffs = [c.real, c.imag] + [0.0] * (dimension - 2)
            return HypercomplexNumber(*coeffs, dimension=dimension)
        
        # If iterable (list, tuple, etc.)
        if hasattr(s, '__iter__') and not isinstance(s, str):
            coeffs = list(s)
            if len(coeffs) < dimension:
                coeffs = coeffs + [0.0] * (dimension - len(coeffs))
            elif len(coeffs) > dimension:
                coeffs = coeffs[:dimension]
            return HypercomplexNumber(*coeffs, dimension=dimension)
        
        # String parsing
        if not isinstance(s, str):
            s = str(s)
        
        s = s.strip()
        s = s.strip('[]{}()')
        
        if not s:
            return HypercomplexNumber(*([0.0] * dimension), dimension=dimension)
        
        # Comma-separated list
        if ',' in s:
            parts = [p.strip() for p in s.split(',') if p.strip()]
            if parts:
                try:
                    coeffs = [float(p) for p in parts]
                    if len(coeffs) < dimension:
                        coeffs = coeffs + [0.0] * (dimension - len(coeffs))
                    elif len(coeffs) > dimension:
                        coeffs = coeffs[:dimension]
                    return HypercomplexNumber(*coeffs, dimension=dimension)
                except ValueError:
                    pass
        
        # Single number
        try:
            coeffs = [float(s)] + [0.0] * (dimension - 1)
            return HypercomplexNumber(*coeffs, dimension=dimension)
        except ValueError:
            pass
        
        # Complex string
        try:
            c = complex(s)
            coeffs = [c.real, c.imag] + [0.0] * (dimension - 2)
            return HypercomplexNumber(*coeffs, dimension=dimension)
        except ValueError:
            pass
    
    except Exception as e:
        warnings.warn(f"Parse error for hypercomplex (dim={dimension}): {e}", RuntimeWarning)
    
    # Fallback: zero
    return HypercomplexNumber(*([0.0] * dimension), dimension=dimension)


def _parse_universal(s: Any, target_type: str) -> Any:
    """
    Universal parser for all number types.
    
    Args:
        s: Input to parse
        target_type: "real", "complex", "quaternion", "octonion", 
                    "sedenion", "pathion", "chingon", "routon", "voudon",
                    "bicomplex", "neutrosophic"
    
    Returns:
        Parsed number
    """
    # Type mapping
    type_map = {
        "real": 1,
        "complex": 2,
        "quaternion": 4,
        "octonion": 8,
        "sedenion": 16,
        "pathion": 32,
        "chingon": 64,
        "routon": 128,
        "voudon": 256
    }
    
    try:
        # Special cases
        if target_type == "bicomplex":
            # Parse bicomplex (4 components: re1, im1, re2, im2)
            if isinstance(s, BicomplexNumber):
                return s
            
            if isinstance(s, str):
                s = s.strip().strip('[]{}()')
            
            # Try to parse as 4 numbers
            if hasattr(s, '__iter__') and not isinstance(s, str):
                coeffs = list(s)
            elif isinstance(s, str) and ',' in s:
                coeffs = [float(p.strip()) for p in s.split(',') if p.strip()]
            else:
                coeffs = [float(s), 0.0, 0.0, 0.0]
            
            if len(coeffs) < 4:
                coeffs = coeffs + [0.0] * (4 - len(coeffs))
            
            z1 = ComplexNumber(coeffs[0], coeffs[1])
            z2 = ComplexNumber(coeffs[2], coeffs[3])
            return BicomplexNumber(z1, z2)
        
        elif target_type == "neutrosophic":
            # Parse neutrosophic (2 components: a, b)
            if isinstance(s, NeutrosophicNumber):
                return s
            
            if isinstance(s, str):
                s = s.strip().strip('[]{}()')
            
            if hasattr(s, '__iter__') and not isinstance(s, str):
                coeffs = list(s)
            elif isinstance(s, str) and ',' in s:
                coeffs = [float(p.strip()) for p in s.split(',') if p.strip()]
            else:
                coeffs = [float(s), 0.0]
            
            if len(coeffs) < 2:
                coeffs = coeffs + [0.0] * (2 - len(coeffs))
            
            return NeutrosophicNumber(coeffs[0], coeffs[1])
        
        # Standard hypercomplex types
        elif target_type in type_map:
            dimension = type_map[target_type]
            return _parse_hypercomplex(s, dimension)
        
        else:
            raise ValueError(f"Unknown target type: {target_type}")
    
    except Exception as e:
        warnings.warn(f"Parse error for {target_type}: {e}", RuntimeWarning)
        
        # Return default value
        defaults = {
            "real": 0.0,
            "complex": ComplexNumber(0, 0),
            "quaternion": HypercomplexNumber(0, 0, 0, 0, dimension=4),
            "octonion": HypercomplexNumber(*([0.0] * 8), dimension=8),
            "sedenion": HypercomplexNumber(*([0.0] * 16), dimension=16),
            "pathion": HypercomplexNumber(*([0.0] * 32), dimension=32),
            "chingon": HypercomplexNumber(*([0.0] * 64), dimension=64),
            "routon": HypercomplexNumber(*([0.0] * 128), dimension=128),
            "voudon": HypercomplexNumber(*([0.0] * 256), dimension=256),
            "bicomplex": BicomplexNumber(ComplexNumber(0, 0), ComplexNumber(0, 0)),
            "neutrosophic": NeutrosophicNumber(0.0, 0.0)
        }
        
        return defaults.get(target_type, None)

# =============================================
# Mathematical Sequences and Functions
# =============================================

def oresme_sequence(n_terms: int) -> List[float]:
    """Generate Oresme sequence: n / 2^n."""
    return [n / (2 ** n) for n in range(1, n_terms + 1)]


def harmonic_numbers(n_terms: int) -> Generator[Fraction, None, None]:
    """Generate harmonic numbers: H_n = 1 + 1/2 + ... + 1/n."""
    current = Fraction(0)
    for n in range(1, n_terms + 1):
        current += Fraction(1, n)
        yield current


def binet_formula(n: int) -> float:
    """Calculate nth Fibonacci number using Binet's formula."""
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    return (phi**n - psi**n) / sqrt5


def generate_cd_chain_names(max_level: int = 8) -> List[str]:
    """Generate names of Cayley-Dickson algebras up to given level."""
    names = ["Real", "Complex", "Quaternion", "Octonion", "Sedenion",
             "Pathion", "Chingon", "Routon", "Voudon"]
    return names[:max_level + 1]
# =============================================
# Example Usage and Tests
# =============================================

if __name__ == "__main__":
    print("Advanced Number Systems Library")
    print("=" * 60)
    
    # Test HypercomplexNumber (Real)
    print("\n1. Testing HypercomplexNumber (Real):")
    r1 = Real(3.14)
    r2 = Real(2.71)
    print(f"   Real(3.14) = {r1}")
    print(f"   Real(2.71) = {r2}")
    print(f"   r1 + r2 = {r1 + r2}")
    print(f"   r1 * r2 = {r1 * r2}")
    
    # Test HypercomplexNumber (Complex)
    print("\n2. Testing HypercomplexNumber (Complex):")
    c1 = Complex(3, 4)
    c2 = Complex(1, 2)
    print(f"   Complex(3, 4) = {c1}")
    print(f"   Complex(1, 2) = {c2}")
    print(f"   c1 + c2 = {c1 + c2}")
    print(f"   c1 * c2 = {c1 * c2}")
    print(f"   |c1| = {c1.norm():.2f}")
    
    # Test HypercomplexNumber (Quaternion)
    print("\n3. Testing HypercomplexNumber (Quaternion):")
    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(5, 6, 7, 8)
    print(f"   Quaternion(1,2,3,4) = {q1}")
    print(f"   Quaternion(5,6,7,8) = {q2}")
    print(f"   q1 + q2 = {q1 + q2}")
    print(f"   q1 * q2 = {q1 * q2}")
    print(f"   Note: Quaternion multiplication is non-commutative")
    print(f"   q2 * q1 = {q2 * q1}")
    print(f"   q1 * q2 == q2 * q1? {q1 * q2 == q2 * q1}")
    
    # Test BicomplexNumber
    print("\n4. Testing BicomplexNumber:")
    bc1 = Bicomplex(1, 2, 3, 4)
    bc2 = Bicomplex(5, 6, 7, 8)
    print(f"   Bicomplex(1,2,3,4) = {bc1}")
    print(f"   Bicomplex(5,6,7,8) = {bc2}")
    print(f"   bc1 + bc2 = {bc1 + bc2}")
    print(f"   bc1 * bc2 = {bc1 * bc2}")
    
    # Test NeutrosophicNumber
    print("\n5. Testing NeutrosophicNumber:")
    n1 = Neutrosophic(3, 2)
    n2 = Neutrosophic(1, 4)
    print(f"   Neutrosophic(3, 2) = {n1}")
    print(f"   n1 + n2 = {n1 + n2}")
    print(f"   n1 * n2 = {n1 * n2}")
    
    # Test mixed operations
    print("\n6. Testing mixed operations:")
    real_num = Real(5.0)
    complex_num = Complex(3, 4)
    print(f"   Real(5) * Complex(3,4) = {real_num * complex_num}")
    print(f"   Complex(3,4) * Real(5) = {complex_num * real_num}")
    
    # Test conversion
    print("\n7. Testing conversions:")
    print(f"   Real(5).to_complex() = {Real(5).to_complex()}")
    print(f"   Complex(3,4).to_complex() = {Complex(3,4).to_complex()}")
    
    # Test with Python built-in types
    print("\n8. Testing with Python built-in types:")
    print(f"   Complex(3,4) + 5 = {Complex(3,4) + 5}")
    print(f"   5 + Complex(3,4) = {5 + Complex(3,4)}")
    print(f"   Complex(3,4) * 2 = {Complex(3,4) * 2}")
    print(f"   2 * Complex(3,4) = {2 * Complex(3,4)}")
    
    print("\n✓ All tests completed successfully!")
