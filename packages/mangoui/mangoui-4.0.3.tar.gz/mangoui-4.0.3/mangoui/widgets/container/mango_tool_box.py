# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 工具箱组件 - 提供统一的工具箱样式和标签页效果
# @Time   : 2025-11-25 10:55
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoToolBox(QToolBox):
    """
    工具箱组件
    
    提供统一的工具箱样式，用于创建可折叠的工具组。
    继承自 QToolBox，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> tool_box = MangoToolBox()
        >>> tool_box.addItem(MangoWidget(parent), "工具组1")
        >>> tool_box.addItem(MangoWidget(parent), "工具组2")
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置工具箱样式
        
        使用全局主题配置，确保样式统一。包括工具箱本身、标签页和滚动区域的样式。
        """
        style = f"""
        QToolBox {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}

        QToolBox::tab {{
            background-color: {THEME.primary_100};
            border: 1px solid {THEME.primary_200};
            color: {THEME.bg_100};
            padding: 8px 12px;
        }}

        QToolBox::tab:selected {{
            background-color: {THEME.primary_200};
            border: 1px solid {THEME.primary_300};
        }}

        QToolBox::tab:hover {{
            background-color: {THEME.primary_200};
        }}

        QToolBox::tab:selected:hover {{
            background-color: {THEME.primary_300};
        }}

        QToolBox::tab:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
            border: 1px solid {THEME.bg_300};
        }}

        QToolBox QScrollArea {{
            background-color: {THEME.bg_100};
            border: none;
        }}
        """
        self.setStyleSheet(style)