# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 表格视图组件 - 提供统一的表格视图样式和交互效果
# @Time   : 2025-11-25 10:30
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoTableView(QTableView):
    """
    表格视图组件
    
    提供统一的表格视图样式，用于显示表格数据。
    继承自 QTableView，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> table_view = MangoTableView()
        >>> model = QStandardItemModel()
        >>> table_view.setModel(model)
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置表格视图样式
        
        使用全局主题配置，确保样式统一。包括正常状态、选中状态、悬停状态和禁用状态的样式。
        """
        style = f"""
        QTableView {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            outline: none;
            gridline-color: {THEME.bg_300};
            selection-background-color: {THEME.primary_100};
            selection-color: {THEME.bg_100};
        }}

        QTableView::item {{
            padding: 8px 12px;
        }}

        QTableView::item:selected {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
        }}

        QTableView::item:hover {{
            background-color: {THEME.bg_200};
        }}

        QTableView::item:selected:hover {{
            background-color: {THEME.primary_200};
        }}

        QHeaderView::section {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
            padding: 8px 12px;
            border: 1px solid {THEME.primary_200};
            font-weight: bold;
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}

        QHeaderView::section:hover {{
            background-color: {THEME.primary_200};
        }}

        QTableView QTableCornerButton::section {{
            background-color: {THEME.primary_100};
            border: 1px solid {THEME.primary_200};
        }}

        QTableView:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QTableView QScrollBar:vertical {{
            border: none;
            background: {THEME.bg_300};
            width: 8px;
            margin: 0px 0px 0px 0px;
            border-radius: 0px;
        }}
        
        QTableView QScrollBar::handle:vertical {{
            background: {THEME.bg_300};
            min-height: 25px;
            border-radius: 4px;
        }}
        
        QTableView QScrollBar:horizontal {{
            border: none;
            background: {THEME.bg_300};
            height: 8px;
            margin: 0px 0px 0px 0px;
            border-radius: 0px;
        }}
        
        QTableView QScrollBar::handle:horizontal {{
            background: {THEME.bg_300};
            min-width: 25px;
            border-radius: 4px;
        }}
        """
        self.setStyleSheet(style)


class MangoTableWidget(QTableWidget):
    """
    表格控件组件（在 mango_table_view.py 中定义）
    
    提供统一的表格控件样式，用于显示和管理表格数据。
    继承自 QTableWidget，使用全局主题配置确保样式统一。
    
    注意：此组件与 mango_table_widget.py 中的 MangoTableWidget 功能相同，
    建议使用独立的 mango_table_widget.py 文件中的组件。
    
    参数:
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> table_widget = MangoTableWidget()
        >>> table_widget.setRowCount(5)
        >>> table_widget.setColumnCount(3)
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置表格控件样式
        
        使用全局主题配置，确保样式统一。包括正常状态、选中状态、悬停状态和禁用状态的样式。
        """
        style = f"""
        QTableWidget {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            outline: none;
            gridline-color: {THEME.bg_300};
            selection-background-color: {THEME.primary_100};
            selection-color: {THEME.bg_100};
        }}

        QTableWidget::item {{
            padding: 8px 12px;
        }}

        QTableWidget::item:selected {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
        }}

        QTableWidget::item:hover {{
            background-color: {THEME.bg_200};
        }}

        QTableWidget::item:selected:hover {{
            background-color: {THEME.primary_200};
        }}

        QHeaderView::section {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
            padding: 8px 12px;
            border: 1px solid {THEME.primary_200};
            font-weight: bold;
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}

        QHeaderView::section:hover {{
            background-color: {THEME.primary_200};
        }}

        QTableWidget QTableCornerButton::section {{
            background-color: {THEME.primary_100};
            border: 1px solid {THEME.primary_200};
        }}

        QTableWidget:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QTableWidget QScrollBar:vertical {{
            border: none;
            background: {THEME.bg_300};
            width: 8px;
            margin: 0px 0px 0px 0px;
            border-radius: 0px;
        }}
        
        QTableWidget QScrollBar::handle:vertical {{
            background: {THEME.bg_300};
            min-height: 25px;
            border-radius: 4px;
        }}
        
        QTableWidget QScrollBar:horizontal {{
            border: none;
            background: {THEME.bg_300};
            height: 8px;
            margin: 0px 0px 0px 0px;
            border-radius: 0px;
        }}
        
        QTableWidget QScrollBar::handle:horizontal {{
            background: {THEME.bg_300};
            min-width: 25px;
            border-radius: 4px;
        }}
        """
        self.setStyleSheet(style)