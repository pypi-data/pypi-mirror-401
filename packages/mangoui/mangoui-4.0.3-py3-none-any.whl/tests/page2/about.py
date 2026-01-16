# -*- coding: utf-8 -*-
# @Description: page2 关于/资讯示例页

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from mangoui.widgets.display import MangoLabel
from mangoui.widgets.layout import MangoVBoxLayout


class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = MangoVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = MangoLabel("关于 & 最新资讯")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600;")

        info = MangoLabel(
            "MangoUI 是基于 Qt 的组件库示例，提供窗口、表单、菜单、图表等常用组件封装。\n"
            "你可以根据需求扩展样式、主题和交互逻辑，以快速搭建桌面端界面。"
        )
        info.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 14px; color: #606266;")

        news_title = MangoLabel("简要资讯")
        news_title.setStyleSheet("font-size: 16px; font-weight: 600;")

        news_list = MangoLabel(
            "• 1/14：主窗口样式2 增加方块菜单与统一标题栏色系演示。\n"
            "• 1/10：组件样式统一，主题变量替换硬编码颜色。\n"
            "• 1/05：新增若干展示与交互示例，方便快速预览。"
        )
        news_list.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        news_list.setWordWrap(True)
        news_list.setStyleSheet("font-size: 14px; color: #606266;")

        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(news_title)
        layout.addWidget(news_list)
        layout.addStretch(1)
