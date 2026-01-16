# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 刻度盘组件 - 提供统一的圆形刻度盘样式和交互效果
# @Time   : 2025-11-25 10:35
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoDial(QDial):
    """
    刻度盘组件
    
    提供统一的圆形刻度盘样式，支持旋转选择数值。
    继承自 QDial，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> dial = MangoDial()
        >>> dial.setRange(0, 100)
        >>> dial.setValue(50)
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.setNotchesVisible(True)
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置刻度盘样式
        
        使用全局主题配置，确保样式统一。包括正常状态、悬停状态、按下状态和禁用状态的样式。
        """
        style = f"""
        QDial {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
        }}

        QDial::handle {{
            background-color: {THEME.primary_100};
            border: 2px solid {THEME.primary_200};
            border-radius: 4px;
            width: 16px;
            height: 16px;
        }}

        QDial::handle:hover {{
            background-color: {THEME.primary_200};
        }}

        QDial::handle:pressed {{
            background-color: {THEME.primary_300};
        }}

        QDial:disabled {{
            background-color: {THEME.bg_200};
        }}

        QDial::handle:disabled {{
            background-color: {THEME.text_200};
            border: 2px solid {THEME.bg_300};
        }}
        """
        self.setStyleSheet(style)