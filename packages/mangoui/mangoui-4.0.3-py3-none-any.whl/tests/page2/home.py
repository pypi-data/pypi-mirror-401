# -*- coding: utf-8 -*-
# @Description: page2 首页演示页

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from mangoui.widgets.display import MangoLabel
from mangoui.widgets.layout import MangoVBoxLayout


class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = MangoVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = MangoLabel("欢迎来到 MangoUI 示例 - 主窗口样式 2")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600;")

        desc = MangoLabel(
            "这是基于 main_2 菜单样式的示例窗口。\n"
            "左侧是方块菜单，顶部和菜单区域同色融合，"
            "你可以点击切换不同演示页面。"
        )
        desc.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px; color: #606266;")

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch(1)
