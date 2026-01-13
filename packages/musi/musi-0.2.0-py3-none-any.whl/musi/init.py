"""
Musi - 基于十二平均律的音乐包
"""

__version__ = "0.2.0"
__author__ = "piacode"

# 从 core 模块导入 musi 实例
from .core import musi

# 将 Musi 类的方法直接暴露为模块级函数
from .core import Musi

# 可选：将常用函数直接暴露
calculate_frequency = musi.calculate_frequency
note = musi.note
scale = musi.scale
chord = musi.chord
play_note = musi.play_note
play_scale = musi.play_scale
play_chord = musi.play_chord
export_scale = musi.export_scale
export_chord = musi.export_chord

# 明确导出
__all__ = [
    'musi',
    'Musi',
    'calculate_frequency',
    'note',
    'scale',
    'chord',
    'play_note',
    'play_scale',
    'play_chord',
    'export_scale',
    'export_chord'
]