# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 字体下拉框组件 - 提供统一的字体选择器样式和交互效果
# @Time   : 2025-11-25 10:40
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoFontComboBox(QFontComboBox):
    """
    字体下拉框组件
    
    提供统一的字体选择器样式，支持从系统字体列表中选择字体。
    继承自 QFontComboBox，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> font_combo = MangoFontComboBox()
        >>> font_combo.setCurrentFont(QFont("Arial"))
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置字体下拉框样式
        
        使用全局主题配置，确保样式统一。包括正常状态、聚焦状态、禁用状态和下拉列表样式。
        """
        style = f"""
        QFontComboBox {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            padding: 8px 12px;
            selection-color: {THEME.bg_100};
            selection-background-color: {THEME.primary_100};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            outline: none;
        }}

        QFontComboBox:focus {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}
        
        QFontComboBox:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QFontComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: {THEME.bg_300};
            border-left-style: solid;
            border-top-right-radius: {THEME.border_radius};
            border-bottom-right-radius: {THEME.border_radius};
        }}

        QFontComboBox::down-arrow {{
            image: url(:/icons/down.svg);
            width: 12px;
            height: 12px;
        }}
        
        QFontComboBox QAbstractItemView {{
            background-color: {THEME.bg_100};
            border: 1px solid {THEME.bg_300};
            border-radius: {THEME.border_radius};
            selection-background-color: {THEME.primary_100};
            selection-color: {THEME.bg_100};
        }}
        """
        self.setStyleSheet(style)
        self.setMinimumHeight(36)