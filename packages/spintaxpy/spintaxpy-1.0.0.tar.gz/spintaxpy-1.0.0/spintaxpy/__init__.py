"""
Spintax - Combinatorial String Generation Library

A library for generating all possible combinations of template strings
with variable elements.
"""

from .spintax import parse, count, choose, range as spintax_range

__all__ = ['parse', 'count', 'choose', 'spintax_range']
__version__ = '1.0.0'
