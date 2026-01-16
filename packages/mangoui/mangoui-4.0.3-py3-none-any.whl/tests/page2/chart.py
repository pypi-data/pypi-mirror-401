# -*- coding: utf-8 -*-
# @Description: page2 图表/数据概要示例页

from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtCore import Qt

from mangoui.widgets.display import MangoLabel
from mangoui.widgets.layout import MangoVBoxLayout
from mangoui.settings.settings import THEME


class ChartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = MangoVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = MangoLabel("图表 & 数据概要")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600;")

        desc = MangoLabel(
            "此处可嵌入折线图、柱状图或统计卡片。\n"
            "当前使用占位区，方便后续替换为真实图表组件。"
        )
        desc.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px; color: #606266;")

        placeholder = QFrame()
        placeholder.setFixedHeight(200)
        placeholder.setStyleSheet(
            f"background: {THEME.bg_200}; border: 1px dashed {THEME.bg_300}; border-radius: {THEME.border_radius};"
        )

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(placeholder)
        layout.addStretch(1)
