# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 数值输入框组件 - 提供统一的整数和浮点数输入框样式
# @Time   : 2025-11-25 10:00
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoSpinBox(QSpinBox):
    """
    整数输入框组件
    
    提供统一的整数输入框样式，支持增减按钮和键盘输入。
    继承自 QSpinBox，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> spin_box = MangoSpinBox()
        >>> spin_box.setRange(0, 100)
        >>> spin_box.setValue(50)
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置整数输入框样式
        
        使用全局主题配置，确保样式统一。包括正常状态、聚焦状态、禁用状态和增减按钮样式。
        """
        style = f"""
        QSpinBox {{
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

        QSpinBox:focus {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}
        
        QSpinBox:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 16px;
            border-left-width: 1px;
            border-left-color: {THEME.bg_300};
            border-left-style: solid;
            border-top-right-radius: {THEME.border_radius};
            background: {THEME.bg_100};
        }}

        QSpinBox::up-button:hover {{
            background: {THEME.bg_200};
        }}

        QSpinBox::up-arrow {{
            image: url(:/icons/up.svg);
            width: 10px;
            height: 10px;
        }}

        QSpinBox::up-arrow:disabled {{
            image: url(:/icons/up_disabled.svg);
        }}

        QSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 16px;
            border-left-width: 1px;
            border-left-color: {THEME.bg_300};
            border-left-style: solid;
            border-bottom-right-radius: {THEME.border_radius};
            background: {THEME.bg_100};
        }}

        QSpinBox::down-button:hover {{
            background: {THEME.bg_200};
        }}

        QSpinBox::down-arrow {{
            image: url(:/icons/down.svg);
            width: 10px;
            height: 10px;
        }}

        QSpinBox::down-arrow:disabled {{
            image: url(:/icons/down_disabled.svg);
        }}
        """
        self.setStyleSheet(style)
        self.setMinimumHeight(36)


class MangoDoubleSpinBox(QDoubleSpinBox):
    """
    浮点数输入框组件
    
    提供统一的浮点数输入框样式，支持增减按钮和键盘输入。
    继承自 QDoubleSpinBox，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> double_spin = MangoDoubleSpinBox()
        >>> double_spin.setRange(0.0, 100.0)
        >>> double_spin.setValue(3.14)
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置浮点数输入框样式
        
        使用全局主题配置，确保样式统一。包括正常状态、聚焦状态、禁用状态和增减按钮样式。
        """
        style = f"""
        QDoubleSpinBox {{
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

        QDoubleSpinBox:focus {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}
        
        QDoubleSpinBox:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QDoubleSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 16px;
            border-left-width: 1px;
            border-left-color: {THEME.bg_300};
            border-left-style: solid;
            border-top-right-radius: {THEME.border_radius};
            background: {THEME.bg_100};
        }}

        QDoubleSpinBox::up-button:hover {{
            background: {THEME.bg_200};
        }}

        QDoubleSpinBox::up-arrow {{
            image: url(:/icons/up.svg);
            width: 10px;
            height: 10px;
        }}

        QDoubleSpinBox::up-arrow:disabled {{
            image: url(:/icons/up_disabled.svg);
        }}

        QDoubleSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 16px;
            border-left-width: 1px;
            border-left-color: {THEME.bg_300};
            border-left-style: solid;
            border-bottom-right-radius: {THEME.border_radius};
            background: {THEME.bg_100};
        }}

        QDoubleSpinBox::down-button:hover {{
            background: {THEME.bg_200};
        }}

        QDoubleSpinBox::down-arrow {{
            image: url(:/icons/down.svg);
            width: 10px;
            height: 10px;
        }}

        QDoubleSpinBox::down-arrow:disabled {{
            image: url(:/icons/down_disabled.svg);
        }}
        """
        self.setStyleSheet(style)
        self.setMinimumHeight(36)