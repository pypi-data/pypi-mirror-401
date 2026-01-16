# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 列表视图组件 - 提供统一的列表视图样式和交互效果
# @Time   : 2025-11-25 10:20
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoListView(QListView):
    """
    列表视图组件
    
    提供统一的列表视图样式，用于显示列表数据。
    继承自 QListView，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> list_view = MangoListView()
        >>> model = QStringListModel(["项目1", "项目2", "项目3"])
        >>> list_view.setModel(model)
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置列表视图样式
        
        使用全局主题配置，确保样式统一。包括正常状态、选中状态、悬停状态和禁用状态的样式。
        """
        style = f"""
        QListView {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            outline: none;
            padding: 2px;
        }}

        QListView::item {{
            padding: 8px 12px;
            border-radius: {THEME.border_radius};
        }}

        QListView::item:selected {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
        }}

        QListView::item:hover {{
            background-color: {THEME.bg_200};
        }}

        QListView::item:selected:hover {{
            background-color: {THEME.primary_200};
        }}

        QListView:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QListView QScrollBar:vertical {{
            border: none;
            background: {THEME.bg_300};
            width: 8px;
            margin: 0px 0px 0px 0px;
            border-radius: 0px;
        }}
        
        QListView QScrollBar::handle:vertical {{
            background: {THEME.bg_300};
            min-height: 25px;
            border-radius: 4px;
        }}
        """
        self.setStyleSheet(style)


class MangoListWidget(QListWidget):
    """
    列表控件组件
    
    提供统一的列表控件样式，用于显示和管理列表项。
    继承自 QListWidget，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> list_widget = MangoListWidget()
        >>> list_widget.addItem("项目1")
        >>> list_widget.addItem("项目2")
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置列表控件样式
        
        使用全局主题配置，确保样式统一。包括正常状态、选中状态、悬停状态和禁用状态的样式。
        """
        style = f"""
        QListWidget {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            outline: none;
            padding: 2px;
        }}

        QListWidget::item {{
            padding: 8px 12px;
            border-radius: {THEME.border_radius};
        }}

        QListWidget::item:selected {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
        }}

        QListWidget::item:hover {{
            background-color: {THEME.bg_200};
        }}

        QListWidget::item:selected:hover {{
            background-color: {THEME.primary_200};
        }}

        QListWidget:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QListWidget QScrollBar:vertical {{
            border: none;
            background: {THEME.bg_300};
            width: 8px;
            margin: 0px 0px 0px 0px;
            border-radius: 0px;
        }}
        
        QListWidget QScrollBar::handle:vertical {{
            background: {THEME.bg_300};
            min-height: 25px;
            border-radius: 4px;
        }}
        """
        self.setStyleSheet(style)