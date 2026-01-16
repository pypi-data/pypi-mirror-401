# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# 从具体的组件模块中导入所需的组件
from mangoui.widgets.menu import (
    MangoTabs, MangoMenuBar, MangoToolBar
)
from mangoui.widgets.display import MangoLabel
from mangoui.widgets.window import MangoScrollArea
from mangoui.widgets.layout import MangoVBoxLayout, MangoGridLayout


class MenuPage(QWidget):
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
        title = MangoLabel("菜单组件展示")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px 0 20px 0;")
        self.scroll_layout.addWidget(title)

        # 使用网格布局组织菜单组件，提高空间利用率
        self.components_grid = MangoGridLayout()
        # 设置网格布局的间距，增加组件之间的间距
        self.components_grid.setSpacing(20)
        self.components_grid.setColumnStretch(1, 1)
        
        # 选项卡组件（原有）
        tabs_label = MangoLabel("选项卡:")
        tabs_label.setMinimumWidth(120)
        self.mango_tabs = MangoTabs()
        self.mango_tabs.setMinimumHeight(200)
        self.mango_tabs.add_tab("标签页1", MangoLabel("标签页1内容"))
        self.mango_tabs.add_tab("标签页2", MangoLabel("标签页2内容"))
        self.mango_tabs.add_tab("标签页3", MangoLabel("标签页3内容"))
        self.components_grid.addWidget(tabs_label, 0, 0)
        self.components_grid.addWidget(self.mango_tabs, 0, 1)

        # 菜单栏组件
        menu_bar_label = MangoLabel("菜单栏:")
        menu_bar_label.setMinimumWidth(120)
        self.mango_menu_bar = MangoMenuBar()
        self.mango_menu_bar.setMinimumHeight(30)
        file_menu = self.mango_menu_bar.addMenu("文件")
        edit_menu = self.mango_menu_bar.addMenu("编辑")
        help_menu = self.mango_menu_bar.addMenu("帮助")
        
        # 文件菜单项
        new_action = file_menu.addAction("新建")
        open_action = file_menu.addAction("打开")
        save_action = file_menu.addAction("保存")
        file_menu.addSeparator()
        exit_action = file_menu.addAction("退出")
        
        # 编辑菜单项
        undo_action = edit_menu.addAction("撤销")
        redo_action = edit_menu.addAction("重做")
        edit_menu.addSeparator()
        cut_action = edit_menu.addAction("剪切")
        copy_action = edit_menu.addAction("复制")
        paste_action = edit_menu.addAction("粘贴")
        
        # 帮助菜单项
        about_action = help_menu.addAction("关于")
        
        self.components_grid.addWidget(menu_bar_label, 1, 0)
        self.components_grid.addWidget(self.mango_menu_bar, 1, 1)

        # 工具栏组件
        tool_bar_label = MangoLabel("工具栏:")
        tool_bar_label.setMinimumWidth(120)
        self.mango_tool_bar = MangoToolBar("工具栏")
        self.mango_tool_bar.setMinimumHeight(40)
        self.mango_tool_bar.addAction("新建", lambda: print("新建"))
        self.mango_tool_bar.addAction("打开", lambda: print("打开"))
        self.mango_tool_bar.addAction("保存", lambda: print("保存"))
        self.mango_tool_bar.addSeparator()
        self.mango_tool_bar.addAction("剪切", lambda: print("剪切"))
        self.mango_tool_bar.addAction("复制", lambda: print("复制"))
        self.mango_tool_bar.addAction("粘贴", lambda: print("粘贴"))
        
        self.components_grid.addWidget(tool_bar_label, 2, 0)
        self.components_grid.addWidget(self.mango_tool_bar, 2, 1)
        
        self.scroll_layout.addLayout(self.components_grid)

        # 设置滚动区域
        self.layout.addWidget(self.scroll_area)