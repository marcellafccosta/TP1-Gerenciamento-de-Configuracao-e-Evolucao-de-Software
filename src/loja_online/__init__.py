"""
Sistema Loja Online - TP1 GCES
Sistema simples de loja online desenvolvido para o TP1.
"""

__version__ = "1.0.0"
__author__ = "Equipe TP1"

from .loja import Loja
from .produto import Produto
from .cliente import Cliente

__all__ = ["Loja", "Produto", "Cliente"]