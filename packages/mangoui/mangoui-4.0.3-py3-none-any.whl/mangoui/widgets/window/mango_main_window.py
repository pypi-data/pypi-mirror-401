# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 主窗口组件 - 提供统一的主窗口基类
# @Time   : 2024-11-17 15:02
# @Author : 毛鹏
from PySide6.QtWidgets import QMainWindow

from mangoui.widgets.layout.mango_layout import MangoVBoxLayout


class MangoMainWindow(QMainWindow):
    """
    主窗口组件
    
    提供统一的主窗口基类，使用 MangoVBoxLayout 作为默认布局。
    继承自 QMainWindow，确保窗口样式统一。
    
    参数:
        parent: 父组件
    
    示例:
        >>> main_window = MangoMainWindow()
        >>> main_window.setCentralWidget(MangoWidget(main_window))
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = MangoVBoxLayout(self)
