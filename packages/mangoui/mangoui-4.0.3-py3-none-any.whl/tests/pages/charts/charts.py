# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# 从具体的组件模块中导入所需的组件
from mangoui.widgets.charts import (
    MangoLinePlot, MangoPiePlot
)
from mangoui.widgets.display import MangoLabel
from mangoui.widgets.window import MangoScrollArea
from mangoui.widgets.layout import MangoVBoxLayout, MangoGridLayout


class ChartsPage(QWidget):
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
        title = MangoLabel("图表组件展示")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px 0 20px 0;")
        self.scroll_layout.addWidget(title)

        # 使用网格布局组织图表组件，提高空间利用率
        self.components_grid = MangoGridLayout()
        # 设置网格布局的间距，增加组件之间的间距
        self.components_grid.setSpacing(20)
        self.components_grid.setColumnStretch(1, 1)
        
        # 折线图
        line_chart_label = MangoLabel("折线图:")
        line_chart_label.setMinimumWidth(120)
        self.line_chart = MangoLinePlot("折线图标题", "Y轴标签", "X轴标签")
        self.line_chart.setMinimumHeight(300)
        self.components_grid.addWidget(line_chart_label, 0, 0)
        self.components_grid.addWidget(self.line_chart, 0, 1)

        # 饼图
        pie_chart_label = MangoLabel("饼图:")
        pie_chart_label.setMinimumWidth(120)
        self.pie_chart = MangoPiePlot()
        self.pie_chart.setMinimumHeight(300)
        self.components_grid.addWidget(pie_chart_label, 1, 0)
        self.components_grid.addWidget(self.pie_chart, 1, 1)
        
        self.scroll_layout.addLayout(self.components_grid)

        # 设置滚动区域
        self.layout.addWidget(self.scroll_area)