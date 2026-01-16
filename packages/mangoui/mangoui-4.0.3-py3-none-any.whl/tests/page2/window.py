# -*- coding: utf-8 -*-
# @Description: page2 窗口组件演示页

from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtCore import Qt

from mangoui.widgets.display import MangoLabel
from mangoui.widgets.layout import MangoVBoxLayout
from mangoui.settings.settings import THEME


class WindowPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = MangoVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = MangoLabel("窗口组件示例")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600;")

        desc = MangoLabel(
            "这里可以放置窗口相关组件的演示，例如卡片、弹窗、布局等。\n"
            "当前仅展示占位内容，实际项目可替换为真实组件。"
        )
        desc.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px; color: #606266;")

        placeholder = QFrame()
        placeholder.setFixedHeight(180)
        placeholder.setStyleSheet(
            f"background: {THEME.bg_200}; border: 1px dashed {THEME.bg_300}; border-radius: {THEME.border_radius};"
        )

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(placeholder)
        layout.addStretch(1)
