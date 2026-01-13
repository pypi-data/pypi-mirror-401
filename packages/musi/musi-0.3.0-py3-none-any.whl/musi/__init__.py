"""
Musi - A music package based on twelve-tone equal temperament
"""

__version__ = "0.3.0"
__author__ = "piacode"

# 导入所有内容
from .main import *

# 导出列表
__all__ = [
    "Musi",
    "musi",
    "calculate_frequency",
    "note",
    "scale",
    "chord",
    "play_note",
    "play_scale",
    "play_chord",
    "export_scale",
    "export_chord"
]