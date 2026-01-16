# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 对话框组件 - 提供统一的对话框样式和交互效果
# @Time   : 2024-08-30 14:51
# @Author : 毛鹏
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoDialog(QDialog):
    """
    对话框组件
    
    提供统一的对话框样式，用于显示模态对话框。
    继承自 QDialog，使用全局主题配置确保样式统一。
    
    参数:
        tips: 对话框标题
        size: 对话框大小元组，默认 (400, 300)
    
    示例:
        >>> dialog = MangoDialog("确认操作", (500, 400))
        >>> dialog.layout.addWidget(MangoLabel("确定要执行此操作吗？"))
    """
    def __init__(self, tips: str, size: tuple = (400, 300)):
        super().__init__()
        self.setWindowTitle(tips)
        self.setFixedSize(*size)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon(':/icons/app_icon.png'))
        
        # 设置样式表
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {THEME.bg_100};
                border-radius: {THEME.border_radius};
                border: 1px solid {THEME.bg_300};
            }}
            
            QDialog QLabel {{
                color: {THEME.text_100};
                font-family: {THEME.font.family};
                font-size: {THEME.font.text_size}px;
            }}
            
            QDialog QPushButton {{
                background-color: {THEME.primary_100};
                border: none;
                border-radius: {THEME.border_radius};
                color: {THEME.bg_100};
                padding: 8px 16px;
                font-family: {THEME.font.family};
                font-size: {THEME.font.text_size}px;
            }}
            
            QDialog QPushButton:hover {{
                background-color: {THEME.primary_200};
            }}
            
            QDialog QPushButton:pressed {{
                background-color: {THEME.primary_300};
            }}
        """)
