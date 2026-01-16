# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# 从具体的组件模块中导入所需的组件
from mangoui.widgets.miscellaneous import (
    MangoCredits, MangoGrips
)
from mangoui.widgets.display import MangoLabel
from mangoui.widgets.window import MangoScrollArea
from mangoui.widgets.layout import MangoVBoxLayout, MangoGridLayout


class MiscellaneousPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = MangoVBoxLayout(self)
        
        # 创建滚动区域以容纳所有组件
        self.scroll_area = MangoScrollArea()
        self.scroll_layout = self.scroll_area.layout
        # 设置滚动布局的边距，增加左右和上下间距
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(20)
        
        # 标题
        title = MangoLabel("其他组件展示")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px 0 20px 0;")
        self.scroll_layout.addWidget(title)

        # 使用网格布局组织其他组件，提高空间利用率
        self.components_grid = MangoGridLayout()
        # 设置网格布局的间距，增加组件之间的间距
        self.components_grid.setSpacing(20)
        self.components_grid.setColumnStretch(1, 1)
        
        # 版权信息组件
        credits_label = MangoLabel("版权信息:")
        credits_label.setMinimumWidth(120)
        self.mango_credits = MangoCredits("Copyright © 2025 芒果测试平台", "1.0.0")
        self.components_grid.addWidget(credits_label, 0, 0)
        self.components_grid.addWidget(self.mango_credits, 0, 1)

        # 调整大小组件
        grips_label = MangoLabel("调整大小组件:")
        grips_label.setMinimumWidth(120)
        self.mango_grips = MangoGrips(self, "bottom_right")
        self.components_grid.addWidget(grips_label, 1, 0)
        self.components_grid.addWidget(self.mango_grips, 1, 1)
        
        self.scroll_layout.addLayout(self.components_grid)

        # 设置滚动区域
        self.layout.addWidget(self.scroll_area)