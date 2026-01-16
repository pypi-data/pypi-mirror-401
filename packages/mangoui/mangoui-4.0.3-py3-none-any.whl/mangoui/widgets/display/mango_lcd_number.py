# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: LCD数字显示组件 - 提供统一的LCD数字显示样式
# @Time   : 2025-11-25 11:15
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoLCDNumber(QLCDNumber):
    """
    LCD数字显示组件
    
    提供统一的LCD数字显示样式，用于显示数字信息。
    继承自 QLCDNumber，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> lcd = MangoLCDNumber()
        >>> lcd.display(123)
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.setSegmentStyle(QLCDNumber.Filled)  # type: ignore
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置LCD数字显示样式
        
        使用全局主题配置，确保样式统一。包括正常状态和禁用状态的样式。
        """
        style = f"""
        QLCDNumber {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            color: {THEME.primary_100};
        }}

        QLCDNumber:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        """
        self.setStyleSheet(style)