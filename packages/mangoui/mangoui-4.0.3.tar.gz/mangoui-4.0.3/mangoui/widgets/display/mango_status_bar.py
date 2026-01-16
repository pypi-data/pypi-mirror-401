# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 状态栏组件 - 提供统一的状态栏样式和交互效果
# @Time   : 2025-11-25 11:10
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoStatusBar(QStatusBar):
    """
    状态栏组件
    
    提供统一的状态栏样式，用于显示应用程序状态信息。
    继承自 QStatusBar，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> status_bar = MangoStatusBar()
        >>> status_bar.showMessage("就绪")
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置状态栏样式
        
        使用全局主题配置，确保样式统一。包括状态栏本身、标签和按钮的样式。
        """
        style = f"""
        QStatusBar {{
            background-color: {THEME.primary_100};
            border-top: 1px solid {THEME.primary_200};
            color: {THEME.bg_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            padding: 4px;
        }}

        QStatusBar:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
            border-top: 1px solid {THEME.bg_300};
        }}

        QStatusBar QLabel {{
            color: {THEME.bg_100};
            background-color: transparent;
        }}

        QStatusBar QPushButton {{
            background-color: {THEME.primary_200};
            color: {THEME.bg_100};
            border: none;
            border-radius: {THEME.border_radius};
            padding: 4px 8px;
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}

        QStatusBar QPushButton:hover {{
            background-color: {THEME.primary_300};
        }}

        QStatusBar QPushButton:pressed {{
            background-color: {THEME.accent_100};
        }}

        QStatusBar QPushButton:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        """
        self.setStyleSheet(style)