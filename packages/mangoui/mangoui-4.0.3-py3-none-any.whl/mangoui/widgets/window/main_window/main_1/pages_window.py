# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 页面窗口管理组件 - 提供统一的页面切换和管理功能
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME
from mangoui.widgets.display.mango_label import MangoLabel


class PagesWindow:
    """
    页面窗口管理组件
    
    提供统一的页面切换和管理功能，使用 QStackedWidget 实现页面切换。
    支持数据加载和页面显示。
    
    参数:
        parent: 父窗口组件
        content_area_left_frame: 内容区域左侧框架
        page_dict: 页面字典，键为页面名称，值为页面类
    
    示例:
        >>> pages_window = PagesWindow(parent, content_frame, page_dict)
        >>> pages_window.set_page("home", {"key": "value"})
    """

    def __init__(self, parent, content_area_left_frame, page_dict):
        self.parent = parent
        self.content_area_left_frame = content_area_left_frame
        self.page_dict = page_dict

        self.loading_indicator = MangoLabel("数据加载中...")
        self.loading_indicator.setAlignment(Qt.AlignCenter)  # type: ignore
        self.loading_indicator.setStyleSheet(f"font-size: 16px; color: {THEME.text_100};")

        self.main_pages_layout = QVBoxLayout(self.content_area_left_frame)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setContentsMargins(0, 0, 0, 0)
        self.main_pages_layout.setAlignment(Qt.AlignTop)  # type: ignore
        self.pages = QStackedWidget(self.content_area_left_frame)
        self.pages.setStyleSheet("background-color: #ffffff; border: none;")
        self.main_pages_layout.addWidget(self.pages)
        QMetaObject.connectSlotsByName(self.content_area_left_frame)

    def set_page(self, page: str, data: dict | None = None):
        """
        设置当前显示的页面
        
        根据页面名称从页面字典中获取页面类，创建页面实例并显示。
        
        参数:
            page: 页面名称
            data: 传递给页面的数据字典，可选
        """
        page_class = self.page_dict.get(page)
        if page_class is not None:
            page = page_class(self.parent)
        else:
            return
        page.data = data if data is not None and isinstance(data, dict) else {}
        if hasattr(page, 'show_data'):
            page.show_data()
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)
        self.parent.page = page