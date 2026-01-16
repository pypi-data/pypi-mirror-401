# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 工具栏组件 - 提供统一的工具栏样式和工具按钮效果
# @Time   : 2025-11-25 11:05
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoToolBar(QToolBar):
    """
    工具栏组件
    
    提供统一的工具栏样式，用于放置工具按钮。
    继承自 QToolBar，使用全局主题配置确保样式统一。
    
    参数:
        title: 工具栏标题
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> tool_bar = MangoToolBar("主工具栏")
        >>> tool_bar.addAction(action)
    """
    def __init__(self, title="", parent=None, **kwargs):
        super().__init__(title, parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置工具栏样式
        
        使用全局主题配置，确保样式统一。包括工具栏本身、工具按钮、分隔符和手柄的样式。
        """
        style = f"""
        QToolBar {{
            background-color: {THEME.bg_100};
            border: 1px solid {THEME.bg_300};
            border-radius: {THEME.border_radius};
            padding: 4px;
            spacing: 4px;
        }}

        QToolBar:disabled {{
            background-color: {THEME.bg_200};
        }}

        QToolBar QToolButton {{
            background-color: {THEME.bg_100};
            border: 1px solid {THEME.bg_300};
            border-radius: {THEME.border_radius};
            padding: 6px 10px;
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}

        QToolBar QToolButton:hover {{
            background-color: {THEME.bg_200};
            border: 1px solid {THEME.primary_100};
        }}

        QToolBar QToolButton:pressed {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
        }}

        QToolBar QToolButton:checked {{
            background-color: {THEME.primary_200};
            color: {THEME.bg_100};
        }}

        QToolBar QToolButton:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}

        QToolBar::separator {{
            width: 1px;
            background-color: {THEME.bg_300};
            margin: 2px;
        }}

        QToolBar::handle {{
            background-color: {THEME.bg_300};
            border: 1px solid {THEME.bg_200};
            border-radius: 2px;
        }}
        """
        self.setStyleSheet(style)