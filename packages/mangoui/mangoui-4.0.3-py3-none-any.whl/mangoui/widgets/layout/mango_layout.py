# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 布局组件 - 提供统一的布局管理器样式和默认对齐方式
# @Time   : 2024-11-17 14:55
# @Author : 毛鹏
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout


class MangoVBoxLayout(QVBoxLayout):
    """
    垂直布局组件
    
    提供统一的垂直布局管理器，默认顶部对齐。
    继承自 QVBoxLayout，确保布局样式统一。
    
    参数:
        parent: 父组件
    
    示例:
        >>> layout = MangoVBoxLayout()
        >>> layout.addWidget(MangoLabel("标签1"))
        >>> layout.addWidget(MangoLabel("标签2"))
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignTop)  # type: ignore


class MangoHBoxLayout(QHBoxLayout):
    """
    水平布局组件
    
    提供统一的水平布局管理器，默认左对齐。
    继承自 QHBoxLayout，确保布局样式统一。
    
    参数:
        parent: 父组件
    
    示例:
        >>> layout = MangoHBoxLayout()
        >>> layout.addWidget(MangoPushButton("按钮1"))
        >>> layout.addWidget(MangoPushButton("按钮2"))
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignLeft)  # type: ignore


class MangoFormLayout(QFormLayout):
    """
    表单布局组件
    
    提供统一的表单布局管理器，默认左对齐。
    继承自 QFormLayout，确保布局样式统一。
    
    参数:
        parent: 父组件
    
    示例:
        >>> layout = MangoFormLayout()
        >>> layout.addRow(MangoLabel("姓名:"), MangoLineEdit("请输入姓名"))
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignLeft)  # type: ignore


class MangoGridLayout(QGridLayout):
    """
    网格布局组件
    
    提供统一的网格布局管理器，默认左对齐。
    继承自 QGridLayout，确保布局样式统一。
    
    参数:
        parent: 父组件
    
    示例:
        >>> layout = MangoGridLayout()
        >>> layout.addWidget(MangoLabel("标签"), 0, 0)
        >>> layout.addWidget(MangoPushButton("按钮"), 0, 1)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignLeft)  # type: ignore