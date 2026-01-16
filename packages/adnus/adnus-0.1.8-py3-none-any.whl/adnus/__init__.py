# src/adnus/__init__.py
"""
adnus (AdNuS): Advanced Number Systems.
A Python library for exploring number systems beyond the standard real and complex numbers.
"""

__version__ = "0.1.7"

# main.py dosyasındaki ana sınıfları ve fonksiyonları buraya import et
from .main import (
    AdvancedNumber,
    BicomplexNumber,
    NeutrosophicNumber,
    NeutrosophicComplexNumber,
    NeutrosophicBicomplexNumber,
    HyperrealNumber,
    oresme_sequence,
    harmonic_numbers,
    binet_formula,
    generate_cayley_dickson_number,
    generate_cd_chain,
    reals, 
    Complex, 
    Quaternion, 
    Octonion, 
    Sedenion, 
    Pathion, 
    Chingon, 
    Routon, 
    Voudon, 
    cayley_dickson_construction, 
    cayley_dickson_algebra
)

# __all__ listesi, "from adnus import *" komutu kullanıldığında nelerin import edileceğini tanımlar.
# Bu, kütüphanenizin genel arayüzünü (public API) belirlemek için iyi bir pratiktir.
__all__ = [
    "AdvancedNumber",
    "BicomplexNumber",
    "NeutrosophicNumber",
    "NeutrosophicComplexNumber",
    "NeutrosophicBicomplexNumber",
    "HyperrealNumber",
    "oresme_sequence",
    "harmonic_numbers",
    "binet_formula",
    "generate_cayley_dickson_number",
    "generate_cd_chain",
    "reals", 
    "Complex", 
    "Quaternion", 
    "Octonion", 
    "Sedenion", 
    "Pathion", 
    "Chingon", 
    "Routon", 
    "Voudon", 
    "cayley_dickson_construction", 
    "cayley_dickson_algebra"
]
