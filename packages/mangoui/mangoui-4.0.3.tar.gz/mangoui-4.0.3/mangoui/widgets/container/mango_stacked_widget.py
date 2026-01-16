# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 堆叠窗口组件 - 提供统一的堆叠窗口样式
# @Time   : 2025-11-25 10:50
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoStackedWidget(QStackedWidget):
    """
    堆叠窗口组件
    
    提供统一的堆叠窗口样式，用于在同一位置显示多个页面。
    继承自 QStackedWidget，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> stacked = MangoStackedWidget()
        >>> stacked.addWidget(MangoWidget(parent))
        >>> stacked.setCurrentIndex(0)
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置堆叠窗口样式
        
        使用全局主题配置，确保样式统一。包括正常状态和禁用状态的样式。
        """
        style = f"""
        QStackedWidget {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
        }}

        QStackedWidget:disabled {{
            background-color: {THEME.bg_200};
        }}
        """
        self.setStyleSheet(style)