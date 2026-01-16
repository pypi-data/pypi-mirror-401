# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 复选框组件 - 提供统一的复选框样式和交互效果
# @Time   : 2024-08-24 17:16
# @Author : 毛鹏

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from mangoui.settings.settings import THEME


class MangoCheckBox(QCheckBox):
    """
    复选框组件
    
    提供统一的复选框样式，支持选中、悬停、禁用等状态。
    继承自 QCheckBox，使用全局主题配置确保样式统一。
    
    参数:
        text: 复选框显示的文本标签
        parent: 父组件
    
    示例:
        >>> checkbox = MangoCheckBox("同意协议")
        >>> checkbox.setChecked(True)
    """
    def __init__(self, text=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.get_style()

    def get_style(self):
        """
        设置复选框样式
        
        使用全局主题配置，确保样式统一。包括正常状态、悬停状态、选中状态和禁用状态的样式。
        """
        style = f"""
        QCheckBox {{
            spacing: 8px;
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}
        
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 4px;
            border: 1px solid {THEME.bg_300};
            background-color: {THEME.bg_100};
        }}
        
        QCheckBox::indicator:hover {{
            border: 1px solid {THEME.primary_100};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {THEME.primary_100};
            border: 1px solid {THEME.primary_100};
            image: url(:/icons/check.svg);
        }}
        
        QCheckBox:disabled {{
            color: {THEME.text_200};
        }}
        
        QCheckBox::indicator:disabled {{
            background-color: {THEME.bg_200};
            border: 1px solid {THEME.bg_300};
        }}
        
        QCheckBox::indicator:checked:disabled {{
            background-color: {THEME.bg_300};
            border: 1px solid {THEME.bg_300};
            image: url(:/icons/check_disabled.svg);
        }}
        """
        self.setStyleSheet(style)

    def isChecked(self):
        """
        获取复选框的选中状态
        
        返回:
            bool: True 表示选中，False 表示未选中
        """
        return super().isChecked()

    def setChecked(self, checked):
        """
        设置复选框的选中状态
        
        参数:
            checked: bool，True 表示选中，False 表示未选中
        """
        super().setChecked(checked)