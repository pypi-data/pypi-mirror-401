"""
HarpiaWatchForest - Sistema de detección de pérdida de cobertura vegetal
Desarrollado por: Elvis Garcia y Yubrany Gonzalez
Organización: Ministerio de Ambiente de Panamá
"""

__version__ = "1.0.0"
__author__ = "Elvis Garcia, Yubrany Gonzalez"
__organization__ = "Ministerio de Ambiente de Panamá"

from .core import (
    listar_corregimientos,
    obtener_hexagonos_corregimiento,
    procesar_corregimiento,
    HarpiaAnalyzer
)

from .config import HarpiaConfig

__all__ = [
    'listar_corregimientos',
    'obtener_hexagonos_corregimiento', 
    'procesar_corregimiento',
    'HarpiaAnalyzer',
    'HarpiaConfig'
]
