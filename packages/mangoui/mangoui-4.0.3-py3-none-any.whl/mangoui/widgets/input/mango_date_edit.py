# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 日期编辑器组件 - 提供统一的日期选择器样式和交互效果
# @Time   : 2025-11-25 10:05
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoDateEdit(QDateEdit):
    """
    日期编辑器组件
    
    提供统一的日期选择器样式，支持日历弹窗和日期选择。
    继承自 QDateEdit，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> date_edit = MangoDateEdit()
        >>> date_edit.setDate(QDate.currentDate())
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.setCalendarPopup(True)
        self.set_stylesheet()
        
    def set_stylesheet(self):
        style = f"""
        QDateEdit {{
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

        QDateEdit:focus {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}
        
        QDateEdit:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QDateEdit::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: {THEME.bg_300};
            border-left-style: solid;
            border-top-right-radius: {THEME.border_radius};
            border-bottom-right-radius: {THEME.border_radius};
        }}

        QDateEdit::down-arrow {{
            image: url(:/icons/down.svg);
            width: 12px;
            height: 12px;
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
        """
        self.setStyleSheet(style)
        self.setMinimumHeight(36)


class MangoDateTimeEdit(QDateTimeEdit):
    """
    日期时间编辑器组件
    
    提供统一的日期时间选择器样式，支持日历弹窗和日期时间选择。
    继承自 QDateTimeEdit，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> datetime_edit = MangoDateTimeEdit()
        >>> datetime_edit.setDateTime(QDateTime.currentDateTime())
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.setCalendarPopup(True)
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置日期时间编辑器样式
        
        使用全局主题配置，确保样式统一。包括正常状态、聚焦状态、禁用状态和日历弹窗样式。
        """
        style = f"""
        QDateTimeEdit {{
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

        QDateTimeEdit:focus {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}
        
        QDateTimeEdit:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QDateTimeEdit::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: {THEME.bg_300};
            border-left-style: solid;
            border-top-right-radius: {THEME.border_radius};
            border-bottom-right-radius: {THEME.border_radius};
        }}

        QDateTimeEdit::down-arrow {{
            image: url(:/icons/down.svg);
            width: 12px;
            height: 12px;
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
        """
        self.setStyleSheet(style)
        self.setMinimumHeight(36)