# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 主窗口类型2 - 使用菜单样式2 的主窗口封装
# @Time   : 2025-01-14
# @Author : 毛鹏

from PySide6.QtGui import QCursor

from mangoui.models.models import MenusModel, AppConfig
from mangoui.widgets.window.main_window.main_2.ui_window import UIWindow2


class MangoMain2Window(UIWindow2):
    """
    主窗口类型2

    基于 `UIWindow2`，提供与 `MangoMain1Window` 类似的使用方式，
    但左侧菜单使用新的样式2。
    """

    def __init__(self, style: AppConfig, menus: MenusModel, page_dict, l=None, **kwargs):
        super().__init__(style, menus, page_dict, l, **kwargs)

    def resizeEvent(self, event):
        """窗口大小变更时，更新四周拖拽区域"""
        self.resize_grips()

    def mousePressEvent(self, event):
        """记录鼠标按下位置，用于窗口拖动"""
        self.drag_pos = QCursor.pos()

