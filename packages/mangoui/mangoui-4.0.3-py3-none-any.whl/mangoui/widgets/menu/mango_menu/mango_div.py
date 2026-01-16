# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 分隔线组件 - 提供统一的分隔线样式
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoDiv(QWidget):
    """
    分隔线组件
    
    提供统一的分隔线样式，用于在界面中创建视觉分隔。
    继承自 QWidget，使用全局主题配置确保样式统一。
    
    参数:
        color: 分隔线颜色，如果为 None 则使用主题背景色
    
    示例:
        >>> div = MangoDiv(THEME.bg_300)
        >>> div = MangoDiv()  # 使用默认颜色
    """
    def __init__(self, color=None):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0)

        self.frame_line = QFrame()
        if color:
            self.frame_line.setStyleSheet(f"background: {color};")
        else:
            self.frame_line.setStyleSheet(f"background: {THEME.bg_300};")

        self.frame_line.setMaximumHeight(1)
        self.frame_line.setMinimumHeight(1)
        self.layout.addWidget(self.frame_line)
        self.setMaximumHeight(0)