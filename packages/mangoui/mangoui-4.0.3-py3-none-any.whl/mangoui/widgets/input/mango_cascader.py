# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 级联选择器组件 - 提供统一的级联选择器样式和交互效果
# @Time   : 2024-09-05 16:24
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from mangoui.models.models import CascaderModel, DialogCallbackModel
from mangoui.settings.settings import THEME


class MangoCascade(QToolButton):
    """
    级联选择器组件
    
    提供统一的级联选择器样式，支持多级菜单选择。
    继承自 QToolButton，使用全局主题配置确保样式统一。
    
    信号:
        click: 当选择改变时触发，传递回调模型
    
    参数:
        placeholder: 占位符文本
        data: 级联数据列表，类型为 CascaderModel
        value: 初始值
        subordinate: 从属键，用于回调模型
        **kwargs: 额外参数，支持 key 用于回调模型
    
    示例:
        >>> data = [CascaderModel(label="分类1", value="1", children=[...])]
        >>> cascade = MangoCascade("请选择", data)
    """
    click = Signal(object)

    def __init__(self,
                 placeholder: str,
                 data: list[CascaderModel],
                 value: str = None,
                 subordinate: str | None = None,
                 **kwargs
                 ):
        super().__init__()
        self.placeholder = placeholder
        self.data: list[CascaderModel] = data
        self.subordinate: str = subordinate
        self.value: str = value
        self.kwargs = kwargs
        self.set_stylesheet()
        # 创建工具按钮
        self.setPopupMode(QToolButton.InstantPopup)  # type: ignore
        self.menu = QMenu()
        self.set_select(self.data)
        self.set_value(self.value)
        self.setMenu(self.menu)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # type: ignore
        self.is_text = False

    def set_text(self, text: str):
        self.menu.clear()
        self.setText(text)
        self.is_text = True

    def show_selection(self, category, value, label):
        self.setText(f'{category}/{label}')
        self.value = value
        if self.subordinate:
            self.click.emit(DialogCallbackModel(
                key=self.kwargs.get('key'),
                value=value,
                subordinate=self.subordinate,
                input_object=self
            ))

    def get_value(self):
        if self.is_text:
            return None
        return self.value

    def set_select(self, data: list[CascaderModel], clear: bool = False):
        self.setText('')
        self.is_text = False
        if clear:
            self.menu.clear()
        if data is None:
            return
        self.data = data
        for cascade in self.data:
            fruits_menu = QMenu(cascade.label, self)
            if cascade.children:
                for fruit in cascade.children:
                    action = fruits_menu.addAction(fruit.label)
                    action.triggered.connect(
                        lambda checked, value=fruit.value, label=fruit.label,
                               cascade_label=cascade.label: self.show_selection(cascade_label,
                                                                                value,
                                                                                label))
            self.menu.addMenu(fruits_menu)

    def set_value(self, value: str):
        if self.data is None or value is None or value == '':
            self.setText('')
            return
        self.value = value
        for i in self.data:
            for e in i.children:
                if e.value == str(value):
                    self.setText(f'{i.label}/{e.label}')

    def set_stylesheet(self):
        style = f'''
              QToolButton {{
                  background-color: {THEME.bg_100}; /* 按钮背景颜色 */
                  border-radius: {THEME.border_radius}; /* 按钮圆角半径 */
                  border: 1px solid {THEME.bg_300}; /* 按钮边框样式 */
                  padding-left: 10px;
                  padding-right: 10px;
                  padding: 5px; /* 按钮内边距 */
                  color: {THEME.text_100};
              }}

              QToolButton:focus {{
                  border: 1px solid {THEME.primary_100}; /* 焦点时边框颜色 */
                  background-color: {THEME.bg_200}; /* 焦点时背景颜色 */
              }}

              QToolButton::menu-indicator {{
                  image: url(:/icons/down.svg); /* 下拉指示器图像 */
              }}

              QMenu {{
                  background-color: {THEME.bg_100}; /* 菜单背景颜色 */
                  border: 1px solid {THEME.bg_300}; /* 菜单边框样式 */
                  padding: 0; /* 菜单内边距 */
              }}

              QMenu::item {{
                  padding: 10px 15px; /* 菜单项的内边距 */
                  color: {THEME.text_100}; /* 菜单项字体颜色 */
              }}

              QMenu::item:selected {{
                  background-color: {THEME.bg_200}; /* 选中菜单项的背景颜色 */
                  color: {THEME.text_100}; /* 选中菜单项的字体颜色 */
              }}
              '''
        self.setStyleSheet(style)
