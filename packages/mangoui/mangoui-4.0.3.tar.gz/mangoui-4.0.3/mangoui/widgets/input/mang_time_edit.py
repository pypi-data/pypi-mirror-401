# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 时间编辑器组件 - 提供统一的时间选择器样式和交互效果
# @Time   : 2024-10-15 14:28
# @Author : 毛鹏
from PySide6.QtWidgets import QTimeEdit

from mangoui.settings.settings import THEME


class MangoTimeEdit(QTimeEdit):
    """
    时间编辑器组件
    
    提供统一的时间选择器样式，支持时间输入和选择。
    继承自 QTimeEdit，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
    
    示例:
        >>> time_edit = MangoTimeEdit()
        >>> time_edit.setTime(QTime.currentTime())
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_style()

    def set_style(self, height=30):
        """
        设置时间编辑器样式
        
        使用全局主题配置，确保样式统一。包括正常状态和聚焦状态的样式。
        
        参数:
            height: 组件最小高度，默认 30px
        """
        self.setStyleSheet(f"""
            QTimeEdit {{
                background-color: {THEME.bg_100};
                border-radius: {THEME.border_radius};
                border: 1px solid {THEME.bg_300};
                padding-left: 10px;
                padding-right: 10px;
                selection-color: {THEME.bg_100};
                selection-background-color: {THEME.primary_200};
                color: {THEME.text_100};
            }}
            
            QTimeEdit:focus {{
                border: 1px solid {THEME.primary_100};
                background-color: {THEME.bg_200};
            }}
            
            QTimeEdit::up-button, QTimeEdit::down-button {{
                border: none; /* 去掉边框 */
                background: transparent; /* 背景透明 */
                width: 0; /* 设置宽度为0 */
                height: 0; /* 设置高度为0 */
                margin: 0; /* 去掉外边距 */
                padding: 0; /* 去掉内边距 */
            }}
        """)
        self.setMinimumHeight(height)