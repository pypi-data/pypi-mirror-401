# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 线性进度条组件 - 提供统一的进度条样式和交互效果
# @Time   : 2025-11-25 11:25
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoProgressBar(QProgressBar):
    """
    线性进度条组件
    
    提供统一的进度条样式，用于显示任务进度。
    继承自 QProgressBar，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> progress = MangoProgressBar()
        >>> progress.setRange(0, 100)
        >>> progress.setValue(50)
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置进度条样式
        
        使用全局主题配置，确保样式统一。包括正常状态、悬停状态和禁用状态的样式。
        """
        style = f"""
        QProgressBar {{
            background-color: {THEME.bg_300};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            text-align: center;
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}

        QProgressBar::chunk {{
            background-color: {THEME.primary_100};
            border-radius: {THEME.border_radius};
        }}

        QProgressBar::chunk:hover {{
            background-color: {THEME.primary_200};
        }}

        QProgressBar:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}

        QProgressBar::chunk:disabled {{
            background-color: {THEME.text_200};
        }}
        """
        self.setStyleSheet(style)
        self.setMinimumHeight(20)