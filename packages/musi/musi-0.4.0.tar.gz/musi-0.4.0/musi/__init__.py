"""
Musi - A music package based on twelve-tone equal temperament
"""

__version__ = \"0.4.0\"
__author__ = \"piacode\"

# 导入 main.py 中的所有内容
from .main import *

# 显式导出所有重要函数和类
__all__ = [
    'Musi',
    'musi',
    'calculate_frequency',
    'note',
    'scale',
    'chord',
    'play_note',
    'play_scale',
    'play_chord',
    'export_scale',
    'export_chord',
    'InvalidNoteError',
    'InvalidScaleTypeError',
    'InvalidChordTypeError',
    'InvalidNoteDurationError',
    'InvalidBPMError',
    'InvalidDirectionError'
]
