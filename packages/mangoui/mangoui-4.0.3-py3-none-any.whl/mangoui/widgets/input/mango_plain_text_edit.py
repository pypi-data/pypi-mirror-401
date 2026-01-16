# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 纯文本编辑器组件 - 提供统一的纯文本编辑器样式和交互效果
# @Time   : 2025-11-25 10:15
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from mangoui.settings.settings import THEME


class MangoPlainTextEdit(QPlainTextEdit):
    """
    纯文本编辑器组件
    
    提供统一的纯文本编辑器样式，支持占位符、值设置和回调功能。
    继承自 QPlainTextEdit，使用全局主题配置确保样式统一。
    包含统一的滚动条样式，与全局主题保持一致。
    
    信号:
        click: 当文本改变时触发，传递文本内容
    
    参数:
        placeholder: 占位符文本
        value: 初始值
        subordinate: 从属键，用于回调模型
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> plain_edit = MangoPlainTextEdit("请输入纯文本", value="初始内容")
        >>> plain_edit.click.connect(lambda v: print(f"文本内容: {v}"))
    """
    click = Signal(object)

    def __init__(self, placeholder="", value: str | None = None, subordinate: str | None = None, parent=None, **kwargs):
        super().__init__(parent)
        self.placeholder = placeholder
        self.value = value
        self.subordinate = subordinate
        self.kwargs = kwargs
        
        if placeholder:
            self.setPlaceholderText(placeholder)
            
        if self.value:
            self.set_value(self.value)
            
        self.set_stylesheet()
        
    def set_value(self, text: str):
        """
        设置文本内容
        
        参数:
            text: 要设置的文本内容
        """
        self.setPlainText(text)
        
    def get_value(self):
        """
        获取文本内容
        
        返回:
            str: 当前编辑器的纯文本内容
        """
        return self.toPlainText()
        
    def set_stylesheet(self):
        """
        设置纯文本编辑器样式
        
        使用全局主题配置，确保样式统一。包括正常状态、聚焦状态、禁用状态和滚动条样式。
        """
        style = f"""
        QPlainTextEdit {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            padding: 8px 12px;
            selection-color: {THEME.bg_100};
            selection-background-color: {THEME.primary_100};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            outline: none;
        }}

        QPlainTextEdit:focus {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}
        
        QPlainTextEdit:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QPlainTextEdit QScrollBar:vertical {{
            border: none;
            background: {THEME.bg_300};
            width: 8px;
            margin: 0px 0px 0px 0px;
            border-radius: 0px;
        }}
        
        QPlainTextEdit QScrollBar::handle:vertical {{
            background: {THEME.bg_300};
            min-height: 25px;
            border-radius: 4px;
        }}
        """
        self.setStyleSheet(style)