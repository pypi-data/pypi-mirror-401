# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 树形控件组件 - 提供统一的树形控件样式和交互效果
# @Time   : 2025-11-25 10:25
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoTreeWidget(QTreeWidget):
    """
    树形控件组件
    
    提供统一的树形控件样式，用于显示和管理层次结构数据。
    继承自 QTreeWidget，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> tree_widget = MangoTreeWidget()
        >>> root = QTreeWidgetItem(tree_widget, ["根节点"])
        >>> child = QTreeWidgetItem(root, ["子节点"])
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置树形控件样式
        
        使用全局主题配置，确保样式统一。包括正常状态、选中状态、悬停状态和禁用状态的样式。
        """
        style = f"""
        QTreeWidget {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            outline: none;
            padding: 2px;
        }}

        QTreeWidget::item {{
            padding: 4px;
            border-radius: {THEME.border_radius};
        }}

        QTreeWidget::item:selected {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
        }}

        QTreeWidget::item:hover {{
            background-color: {THEME.bg_200};
        }}

        QTreeWidget:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        """
        self.setStyleSheet(style)