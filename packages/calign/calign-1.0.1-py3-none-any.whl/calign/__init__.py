"""
Proprietary - All rights reserved
Calign - Epitope Alignment Tool - A Python package for aligning epitopes to protein sequences and generating visualization heatmaps.

Powered by Authors:
André Luiz Caliari Costa;
Leonardo Pereira de Araújo;
Evandro Neves Silva;
Patrícia Paiva Corsetti;
Leonardo Augusto de Almeida. 
================================

"""

__version__ = "1.0.0"
__author__ = "André Luiz Caliari Costa, Leonardo Pereira de Araújo, Evandro Neves Silva, Patrícia Paiva Corsetti, Leonardo Augusto de Almeida"
__email__ = "andre.costa@sou.unifal-mg.edu.br"

from .core import align_epitopes

__all__ = ["align_epitopes"]