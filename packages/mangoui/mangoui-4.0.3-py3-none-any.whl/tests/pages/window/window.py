# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# 从具体的组件模块中导入所需的组件
from mangoui.widgets.window import (
    MangoDialog, MangoFrame, MangoTree, MangoScrollArea
)
from mangoui.widgets.display import MangoLabel
from mangoui.widgets.input import MangoPushButton
from mangoui.widgets.layout import MangoVBoxLayout, MangoGridLayout


class WindowPage(QWidget):
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
        title = MangoLabel("窗口组件展示")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px 0 20px 0;")
        self.scroll_layout.addWidget(title)

        # 使用网格布局组织窗口组件，提高空间利用率
        self.components_grid = MangoGridLayout()
        # 设置网格布局的间距，增加组件之间的间距
        self.components_grid.setSpacing(20)
        self.components_grid.setColumnStretch(1, 1)
        
        # 对话框组件
        dialog_label = MangoLabel("对话框:")
        dialog_label.setMinimumWidth(120)
        dialog_btn = MangoPushButton("打开对话框")
        dialog_btn.clicked.connect(self.show_dialog)
        self.components_grid.addWidget(dialog_label, 0, 0)
        self.components_grid.addWidget(dialog_btn, 0, 1)

        # 框架组件
        frame_label = MangoLabel("框架:")
        frame_label.setMinimumWidth(120)
        self.mango_frame = MangoFrame(self)
        self.mango_frame.setMinimumHeight(150)
        # 复用 MangoFrame 自带的 layout，避免重复给同一个控件设置布局导致 Qt 警告
        frame_layout = self.mango_frame.layout
        frame_layout.addWidget(MangoLabel("框架内容"))
        self.components_grid.addWidget(frame_label, 1, 0)
        self.components_grid.addWidget(self.mango_frame, 1, 1)

        # 树组件
        tree_label = MangoLabel("树组件:")
        tree_label.setMinimumWidth(120)
        self.mango_tree = MangoTree("树组件标题")
        self.mango_tree.setMinimumHeight(150)
        tree_layout = MangoVBoxLayout(self.mango_tree)
        tree_layout.addWidget(MangoLabel("树组件内容"))
        self.components_grid.addWidget(tree_label, 2, 0)
        self.components_grid.addWidget(self.mango_tree, 2, 1)
        
        self.scroll_layout.addLayout(self.components_grid)

        # 设置滚动区域
        self.layout.addWidget(self.scroll_area)

    def show_dialog(self):
        dialog = MangoDialog(self)
        dialog.setWindowTitle("测试对话框")
        layout = MangoVBoxLayout(dialog)
        layout.addWidget(MangoLabel("这是一个测试对话框"))
        ok_btn = MangoPushButton("确定")
        ok_btn.clicked.connect(dialog.accept)
        layout.addWidget(ok_btn)
        dialog.exec()