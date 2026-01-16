# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 多选下拉框组件 - 提供统一的多选下拉框样式和交互效果
# @Time   : 2024-09-04 17:32
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.models.models import ComboBoxDataModel, DialogCallbackModel
from mangoui.settings.settings import THEME


class MangoComboBoxMany(QComboBox):
    """
    多选下拉框组件
    
    提供统一的多选下拉框样式，支持多选项选择和对话框显示。
    继承自 QComboBox，使用全局主题配置确保样式统一。
    
    信号:
        click: 当选择改变时触发
    
    参数:
        placeholder: 占位符文本
        data: 选项数据列表，类型为 ComboBoxDataModel
        value: 初始值
        parent: 父组件
    
    示例:
        >>> data = [ComboBoxDataModel(id="1", name="选项1")]
        >>> combo = MangoComboBoxMany("请选择", data)
    """
    click = Signal(object)

    def __init__(self,
                 placeholder: str,
                 data: list[ComboBoxDataModel],
                 value: str = None,
                 parent=None):
        super().__init__(parent)
        self.dialog = None
        self.data = data
        self.parent = parent

        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.list_widget = QListWidget()
        self.list_widget.setContentsMargins(0, 0, 0, 0)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.list_widget)
        self.populate_list_widget()
        if placeholder:
            self.lineEdit().setPlaceholderText(placeholder)
            # 设置默认选项
        if value is not None:
            self.set_value(value)
        self.set_stylesheet()

    def populate_list_widget(self):
        """
        填充列表控件
        
        根据数据模型创建列表项，每个项都可以被选中。
        """
        for option in self.data:
            item = QListWidgetItem(option.name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # type: ignore
            item.setCheckState(Qt.Unchecked)  # type: ignore
            self.list_widget.addItem(item)

    def showPopup(self):
        """
        显示下拉对话框
        
        当用户点击下拉箭头时，显示一个包含可选列表的对话框。
        """
        if self.dialog is None:
            self.dialog = QDialog(self)
        else:
            self.dialog.setWindowTitle("选择项目")
            self.dialog.setFixedSize(200, 150)
            self.dialog.setLayout(self.layout)
            self.list_widget.itemChanged.connect(self.update_display)
            self.dialog.accepted.connect(self.update_display)
            self.dialog.exec()

    def update_display(self):
        """
        更新显示文本
        
        根据选中的项更新输入框显示的文本，多个选项用逗号分隔。
        """
        selected_items = [self.list_widget.item(i).text() for i in range(self.list_widget.count()) if
                          self.list_widget.item(i).checkState() == Qt.Checked]  # type: ignore
        if selected_items:
            self.lineEdit().setText(", ".join(selected_items))
        else:
            self.lineEdit().clear()
            self.lineEdit().setPlaceholderText("选择项目")

    def get_value(self):
        """
        获取选中的值列表
        
        返回:
            list: 选中项的文本列表
        """
        return [self.list_widget.item(i).text() for i in range(self.list_widget.count()) if
                self.list_widget.item(i).checkState() == Qt.Checked]  # type: ignore

    def set_value(self, value):
        """
        设置选中的值
        
        参数:
            value: 要设置的值，可以是字符串（会被解析为列表）或列表
        """
        try:
            value_list = eval(value) if isinstance(value, str) else value
        except Exception:
            value_list = [value]
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.text() in value_list:
                item.setCheckState(Qt.Checked)  # type: ignore
            else:
                item.setCheckState(Qt.Unchecked)  # type: ignore
        selected_values = [item.text() for i in range(self.list_widget.count()) if
                           self.list_widget.item(i).checkState() == Qt.Checked]  # type: ignore
        if selected_values:
            self.lineEdit().setText(", ".join(selected_values))
        else:
            self.lineEdit().clear()
            self.lineEdit().setPlaceholderText("选择项目")

        self.update_display()

    def set_stylesheet(self, icon=':/icons/down.svg'):
        """
        设置下拉框样式
        
        使用全局主题配置，确保样式统一。包括正常状态、聚焦状态、禁用状态和下拉列表样式。
        
        参数:
            icon: 下拉箭头图标路径，默认使用主题图标
        """
        style = f'''
        QComboBox {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_200};
            padding: 8px 12px;
            padding-right: 35px; /* 为下拉箭头留出更多空间 */
            selection-color: {THEME.bg_100};
            selection-background-color: {THEME.primary_100};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            outline: none;
        }}
        
        QComboBox:focus {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}
        
        QComboBox:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: {THEME.bg_200};
            border-left-style: solid;
            border-top-right-radius: {THEME.border_radius};
            border-bottom-right-radius: {THEME.border_radius};
        }}
        
        QComboBox::down-arrow {{
            image: url({icon});
            width: 20px;
            height: 20px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {THEME.bg_100};
            border: 1px solid {THEME.bg_200};
            border-radius: {THEME.border_radius};
            selection-background-color: {THEME.primary_200};
            selection-color: {THEME.text_100};
            outline: none;
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: 8px 12px;
            color: {THEME.text_100};
        }}
        
        QComboBox QAbstractItemView::item:selected {
            background-color: {THEME.primary_200};
            color: {THEME.text_100};
        }
        
        /* 滚动条样式 - 与 MangoScrollArea 保持一致 */
        QComboBox QAbstractItemView QScrollBar:vertical {
            border: none;
            background: {THEME.bg_300};
            width: 8px;
            margin: 21px 0;
            border-radius: 0px;
        }
        
        QComboBox QAbstractItemView QScrollBar::handle:vertical {
            background: {THEME.bg_300};
            min-height: 25px;
            border-radius: 4px;
        }
        
        QComboBox QAbstractItemView QScrollBar::add-line:vertical {
            border: none;
            background: {THEME.bg_300};
            height: 20px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        
        QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
            border: none;
            background: {THEME.bg_300};
            height: 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        
        QComboBox QAbstractItemView QScrollBar:horizontal {
            border: none;
            background: {THEME.bg_300};
            height: 8px;
            margin: 0px 21px;
            border-radius: 0px;
        }
        
        QComboBox QAbstractItemView QScrollBar::handle:horizontal {
            background: {THEME.bg_300};
            min-width: 25px;
            border-radius: 4px;
        }
        
        QComboBox QAbstractItemView QScrollBar::add-line:horizontal {
            border: none;
            background: {THEME.bg_300};
            width: 20px;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }
        
        QComboBox QAbstractItemView QScrollBar::sub-line:horizontal {
            border: none;
            background: {THEME.bg_300};
            width: 20px;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }
        '''
        self.setStyleSheet(style)
        self.setMinimumHeight(36)  # 设置最小高度


class MangoComboBox(QComboBox):
    """
    下拉选择框组件
    
    提供统一的下拉选择框样式，支持单选、占位符和回调功能。
    继承自 QComboBox，使用全局主题配置确保样式统一。
    
    信号:
        click: 当选择改变时触发，传递回调模型或值
    
    参数:
        placeholder: 占位符文本
        data: 选项数据列表，类型为 ComboBoxDataModel
        value: 初始值，可以是整数或字符串
        subordinate: 从属键，用于回调模型
        is_form: 是否为表单模式，默认 True
        **kwargs: 额外参数，支持 key 用于回调模型
    
    示例:
        >>> data = [ComboBoxDataModel(id="1", name="选项1")]
        >>> combo = MangoComboBox("请选择", data, value="1")
    """
    click = Signal(object)

    def __init__(
            self,
            placeholder: str,
            data: list[ComboBoxDataModel],
            value: int | str = None,
            subordinate: str | None = None,
            is_form: bool = True,
            **kwargs,
    ):
        super().__init__()
        self.kwargs = kwargs
        self.placeholder = placeholder
        self.data = data
        self.value = value
        self.subordinate = subordinate
        self.is_form = is_form
        # 设置样式表
        self.set_stylesheet()
        self.currentIndexChanged.connect(self.combo_box_changed)
        self.set_select(self.data)
        self.setCurrentIndex(-1)
        self.set_value(self.value)
        if self.placeholder:
            self.setPlaceholderText(self.placeholder)

    def get_value(self):
        """
        获取当前选中项的值
        
        返回:
            str: 选中项的 id，如果未选中则返回 None
        """
        value = self.currentText()
        if self.data:
            data_dict = {item.name: item.id for item in self.data}
            return data_dict.get(value)

    def set_select(self, data: list[ComboBoxDataModel], clear: bool = False):
        """
        设置选项列表
        
        参数:
            data: 选项数据列表
            clear: 是否先清空现有选项，默认 False
        """
        if clear:
            self.clear()
        if data:
            self.data = data
            self.addItems([i.name for i in data])

    def set_value(self, value: str):
        """
        设置当前选中项的值
        
        参数:
            value: 要设置的项的 id
        """
        if value is not None and value != '':
            for i in self.data:
                if i.id == str(value):
                    self.value = value
                    self.setCurrentText(i.name)
                    break
            else:
                self.value = ''
                self.setCurrentText('')
        elif value == '':
            self.value = ''
            self.setCurrentText('')

    def combo_box_changed(self, data):
        """
        下拉框选择改变时的回调
        
        当用户选择不同选项时触发，根据是否为表单模式和是否有从属键决定发送回调模型或直接发送值。
        
        参数:
            data: 选择改变的索引
        """
        if self.is_form:
            if self.subordinate:
                self.click.emit(DialogCallbackModel(
                    key=self.kwargs.get('key'),
                    value=self.get_value(),
                    subordinate=self.subordinate,
                    input_object=self
                ))
        else:
            self.click.emit(self.get_value())

    def set_stylesheet(self, icon=':/icons/down.svg'):
        """
        设置下拉框样式
        
        使用全局主题配置，确保样式统一。包括正常状态、聚焦状态、禁用状态和下拉列表样式。
        
        参数:
            icon: 下拉箭头图标路径，默认使用主题图标
        """
        style = f'''
        QComboBox {{
            background-color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            border: 1px solid {THEME.bg_300};
            padding: 8px 12px;
            padding-right: 35px; /* 为下拉箭头留出更多空间 */
            selection-color: {THEME.bg_100};
            selection-background-color: {THEME.primary_100};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
            outline: none;
        }}
        
        QComboBox:focus {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}
        
        QComboBox:disabled {{
            background-color: {THEME.bg_200};
            color: {THEME.text_200};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: {THEME.bg_300};
            border-left-style: solid;
            border-top-right-radius: {THEME.border_radius};
            border-bottom-right-radius: {THEME.border_radius};
        }}
        
        QComboBox::down-arrow {{
            image: url({icon});
            width: 20px;
            height: 20px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {THEME.bg_100};
            border: 1px solid {THEME.bg_300};
            border-radius: {THEME.border_radius};
            selection-background-color: {THEME.primary_200};
            selection-color: {THEME.text_100};
            outline: none;
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: 8px 12px;
            color: {THEME.text_100};
        }}
        
        QComboBox QAbstractItemView::item:selected {{
            background-color: {THEME.primary_200};
            color: {THEME.text_100};
        }}
        
        /* 滚动条样式 - 与 MangoScrollArea 保持一致 */
        QComboBox QAbstractItemView QScrollBar:vertical {{
            border: none;
            background: {THEME.bg_300};
            width: 8px;
            margin: 21px 0;
            border-radius: 0px;
        }}
        
        QComboBox QAbstractItemView QScrollBar::handle:vertical {{
            background: {THEME.bg_300};
            min-height: 25px;
            border-radius: 4px;
        }}
        
        QComboBox QAbstractItemView QScrollBar::add-line:vertical {{
            border: none;
            background: {THEME.bg_300};
            height: 20px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }}
        
        QComboBox QAbstractItemView QScrollBar::sub-line:vertical {{
            border: none;
            background: {THEME.bg_300};
            height: 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }}
        
        QComboBox QAbstractItemView QScrollBar:horizontal {{
            border: none;
            background: {THEME.bg_300};
            height: 8px;
            margin: 0px 21px;
            border-radius: 0px;
        }}
        
        QComboBox QAbstractItemView QScrollBar::handle:horizontal {{
            background: {THEME.bg_300};
            min-width: 25px;
            border-radius: 4px;
        }}
        
        QComboBox QAbstractItemView QScrollBar::add-line:horizontal {{
            border: none;
            background: {THEME.bg_300};
            width: 20px;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }}
        
        QComboBox QAbstractItemView QScrollBar::sub-line:horizontal {{
            border: none;
            background: {THEME.bg_300};
            width: 20px;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }}
        '''
        self.setStyleSheet(style)
        self.setMinimumHeight(36)  # 设置最小高度
