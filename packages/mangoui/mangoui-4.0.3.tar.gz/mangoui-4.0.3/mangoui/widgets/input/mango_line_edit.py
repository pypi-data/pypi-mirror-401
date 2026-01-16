# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 单行文本输入框组件 - 提供统一的输入框样式和交互效果
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from mangoui.models.models import DialogCallbackModel
from mangoui.settings.settings import THEME


class MangoLineEdit(QLineEdit):
    """
    单行文本输入框组件
    
    提供统一的输入框样式，支持占位符、密码模式、值设置和回调功能。
    继承自 QLineEdit，使用全局主题配置确保样式统一。
    
    信号:
        click: 当输入完成或失去焦点时触发，传递输入值或回调模型
    
    参数:
        placeholder: 占位符文本
        value: 初始值
        subordinate: 从属键，用于回调模型
        is_password: 是否为密码输入框
        **kwargs: 额外参数，支持 key 用于回调模型
    
    示例:
        >>> line_edit = MangoLineEdit("请输入内容", value="初始值")
        >>> line_edit.click.connect(lambda v: print(f"输入值: {v}"))
    """
    click = Signal(object)
    mouse_remove = Signal(object)

    def __init__(
            self,
            placeholder,
            value: str | None = None,
            subordinate: str | None = None,
            is_password: bool = False,
            **kwargs
    ):
        super().__init__()
        self.editingFinished.connect(self.line_edit_changed)
        self.subordinate = subordinate
        self.value = value
        self.kwargs = kwargs
        if is_password:
            self.setEchoMode(QLineEdit.Password)  # type: ignore
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.set_value(self.value)
        self.set_stylesheet()

    def get_value(self):
        """
        获取输入框的值
        
        返回:
            str: 当前输入框的文本内容
        """
        return self.text()

    def set_value(self, value):
        """
        设置输入框的值
        
        参数:
            value: 要设置的值，可以是字符串或 None
        """
        self.value = value
        if self.value is not None:
            self.setText(str(self.value))

    def line_edit_changed(self):
        """
        输入框内容改变时的回调
        
        当用户完成编辑时触发，根据是否有从属键决定发送回调模型或直接发送值。
        """
        if self.subordinate:
            self.click.emit(DialogCallbackModel(
                key=self.kwargs.get('key'),
                value=self.text(),
                subordinate=self.subordinate,
                input_object=self
            ))
        else:
            self.click.emit(self.get_value())

    def focusOutEvent(self, event):
        """
        失去焦点事件处理
        
        当输入框失去焦点时，触发 click 信号发送当前值。
        
        参数:
            event: 焦点事件对象
        """
        self.click.emit(self.get_value())
        super().focusOutEvent(event)

    def set_stylesheet(self):
        """
        设置输入框样式
        
        使用全局主题配置，确保样式统一。包括正常状态、聚焦状态和禁用状态的样式。
        """
        style = f"""
        QLineEdit {{
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

        QLineEdit:focus {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}
        
        QLineEdit:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        """
        self.setStyleSheet(style)
        self.setMinimumHeight(36)
