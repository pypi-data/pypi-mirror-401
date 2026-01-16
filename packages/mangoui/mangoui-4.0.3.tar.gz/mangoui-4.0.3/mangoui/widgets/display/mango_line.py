# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 虚线分隔组件 - 提供统一的虚线分隔样式
# @Time   : 2025-03-07 20:18
# @Author : 毛鹏
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QFrame

from mangoui.settings.settings import THEME


class MangoDashedLine(QWidget):
    """
    虚线分隔组件
    
    提供统一的虚线分隔样式，支持可选的中间文本标签。
    继承自 QWidget，使用全局主题配置确保样式统一。
    
    参数:
        text: 可选的中间文本标签
        parent: 父组件
    
    示例:
        >>> line = MangoDashedLine("或")
        >>> line = MangoDashedLine()  # 无文本的虚线
    """
    def __init__(self, text=None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        left_line = QFrame()
        left_line.setFrameShape(QFrame.HLine)
        left_line.setFrameShadow(QFrame.Sunken)
        left_line.setStyleSheet(f"border: 1px dashed {THEME.text_200}; margin: 0; padding: 0;")

        right_line = QFrame()
        right_line.setFrameShape(QFrame.HLine)
        right_line.setFrameShadow(QFrame.Sunken)
        right_line.setStyleSheet(f"border: 1px dashed {THEME.text_200}; margin: 0; padding: 0;")
        if text:
            label = QLabel(text)

            layout.addWidget(left_line, 1)
            layout.addWidget(label)  # 文本居中
            layout.addWidget(right_line, 1)
        else:
            layout.addWidget(left_line)

        # 设置布局
        self.setLayout(layout)