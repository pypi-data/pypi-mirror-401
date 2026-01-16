# -*- coding: utf-8 -*-
# @Description: page2 表单示例页

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from mangoui.widgets.input import MangoLineEdit, MangoComboBox, MangoTextEdit
from mangoui.widgets.display import MangoLabel
from mangoui.widgets.layout import MangoVBoxLayout, MangoFormLayout
from mangoui.models.models import ComboBoxDataModel


class FormPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = MangoVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = MangoLabel("表单示例")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600;")

        form = MangoFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignTop)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(12)

        name_edit = MangoLineEdit("请输入姓名")
        form.addRow("姓名：", name_edit)

        type_data = [
            ComboBoxDataModel(id="suggestion", name="建议"),
            ComboBoxDataModel(id="consultation", name="咨询"),
            ComboBoxDataModel(id="feedback", name="反馈"),
        ]
        type_combo = MangoComboBox("请选择类型", type_data)
        form.addRow("类型：", type_combo)

        content_edit = MangoTextEdit("请输入内容...")
        content_edit.setFixedHeight(120)
        form.addRow("内容：", content_edit)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addStretch(1)
