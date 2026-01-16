# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 日历控件组件 - 提供统一的日历控件样式和交互效果
# @Time   : 2025-11-25 11:20
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoCalendarWidget(QCalendarWidget):
    """
    日历控件组件
    
    提供统一的日历控件样式，用于日期选择。
    继承自 QCalendarWidget，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> calendar = MangoCalendarWidget()
        >>> calendar.setSelectedDate(QDate.currentDate())
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置日历控件样式
        
        使用全局主题配置，确保样式统一。包括日历本身、按钮、菜单和日期项的样式。
        """
        style = f"""
        QCalendarWidget {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
        }}

        QCalendarWidget QToolButton {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
            border: none;
            border-radius: {THEME.border_radius};
            padding: 4px;
            font-weight: bold;
        }}

        QCalendarWidget QToolButton:hover {{
            background-color: {THEME.primary_200};
        }}

        QCalendarWidget QToolButton:pressed {{
            background-color: {THEME.primary_300};
        }}

        QCalendarWidget QToolButton:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}

        QCalendarWidget QMenu {{
            background-color: {THEME.bg_100};
            border: 1px solid {THEME.bg_300};
            border-radius: {THEME.border_radius};
        }}

        QCalendarWidget QMenu::item {{
            padding: 4px 12px;
            background-color: transparent;
            color: {THEME.text_100};
        }}

        QCalendarWidget QMenu::item:selected {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
        }}

        QCalendarWidget QMenu::item:disabled {{
            color: {THEME.text_200};
        }}

        QCalendarWidget QWidget {{
            alternate-background-color: {THEME.bg_200};
        }}

        QCalendarWidget QAbstractItemView:enabled {{
            font-size: {THEME.font.text_size}px;
            color: {THEME.text_100};
            background-color: {THEME.bg_100};
            selection-background-color: {THEME.primary_100};
            selection-color: {THEME.bg_100};
        }}

        QCalendarWidget QAbstractItemView:disabled {{
            color: {THEME.text_200};
        }}

        QCalendarWidget QAbstractItemView:selected {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
        }}
        """
        self.setStyleSheet(style)