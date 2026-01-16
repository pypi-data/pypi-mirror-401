# -*- coding: utf-8 -*-
# @Description: 简易"模拟请求"页，使用 Python 标准库 http 发送请求

import json
import urllib.request
import urllib.error

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from mangoui.widgets.input import (
    MangoLineEdit, MangoComboBox, MangoTextEdit, MangoPushButton
)
from mangoui.widgets.display import MangoLabel
from mangoui.widgets.layout import (
    MangoVBoxLayout, MangoHBoxLayout, MangoFormLayout
)
from mangoui.models.models import ComboBoxDataModel


class RequestPage(QWidget):
    """
    一个简易的“模拟请求”页面，类似轻量版 Postman。
    仅使用 Python 标准库 urllib 请求，方便演示，不依赖第三方。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = MangoVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = MangoLabel("模拟请求（标准库 urllib）")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        # 表单区域
        form = MangoFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setContentsMargins(0, 0, 0, 0)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(8)

        # 创建方法下拉框数据
        method_data = [
            ComboBoxDataModel(id="GET", name="GET"),
            ComboBoxDataModel(id="POST", name="POST"),
            ComboBoxDataModel(id="PUT", name="PUT"),
            ComboBoxDataModel(id="DELETE", name="DELETE"),
        ]
        self.method = MangoComboBox("请选择方法", method_data, value="GET")

        self.url_edit = MangoLineEdit("https://httpbin.org/get")

        self.headers_edit = MangoTextEdit('可选：JSON 格式的请求头，如 {"User-Agent": "Demo"}')
        self.headers_edit.setFixedHeight(80)

        self.body_edit = MangoTextEdit("可选：请求体（文本/json）")
        self.body_edit.setFixedHeight(120)

        form.addRow("方法：", self.method)
        form.addRow("URL：", self.url_edit)
        form.addRow("Headers：", self.headers_edit)
        form.addRow("Body：", self.body_edit)
        layout.addLayout(form)

        # 操作区
        btn_row = MangoHBoxLayout()
        btn_row.addStretch(1)
        self.send_btn = MangoPushButton("发送请求")
        self.send_btn.clicked.connect(self.send_request)
        btn_row.addWidget(self.send_btn)
        layout.addLayout(btn_row)

        # 结果区域
        self.status_label = MangoLabel("状态：未发送")
        self.status_label.setStyleSheet("color: #606266;")
        self.response_view = MangoTextEdit("响应结果将显示在这里")
        self.response_view.setReadOnly(True)
        self.response_view.setMinimumHeight(220)

        layout.addWidget(self.status_label)
        layout.addWidget(self.response_view)
        layout.addStretch(1)

    def send_request(self):
        url = self.url_edit.get_value().strip()
        if not url:
            self.status_label.setText("状态：请填写 URL")
            return

        method = self.method.get_value() or "GET"
        method = method.upper()
        data_bytes = None

        body_text = self.body_edit.get_value()
        if body_text:
            data_bytes = body_text.encode("utf-8")

        headers = {}
        headers_text = self.headers_edit.get_value().strip()
        if headers_text:
            try:
                headers = json.loads(headers_text)
                if not isinstance(headers, dict):
                    raise ValueError("headers 必须是 JSON 对象")
            except Exception as e:
                self.status_label.setText(f"状态：Headers 解析失败 - {e}")
                return

        req = urllib.request.Request(url=url, data=data_bytes, method=method, headers=headers)

        try:
            with urllib.request.urlopen(req) as resp:
                status = resp.status
                resp_body = resp.read()
                try:
                    decoded = resp_body.decode("utf-8", errors="replace")
                except Exception:
                    decoded = str(resp_body)
                self.status_label.setText(f"状态：{status}")
                self.response_view.set_value(decoded)
        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                err_body = str(e)
            self.status_label.setText(f"状态：HTTP {e.code}")
            self.response_view.set_value(err_body)
        except Exception as e:
            self.status_label.setText(f"状态：请求异常 - {e}")
            self.response_view.set_value("")
