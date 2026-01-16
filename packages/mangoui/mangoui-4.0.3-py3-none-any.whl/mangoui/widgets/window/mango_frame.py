# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 框架组件 - 提供统一的框架容器样式和阴影效果
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoFrame(QFrame):
    """
    框架组件
    
    提供统一的框架容器样式，支持自定义布局、边距和阴影效果。
    继承自 QFrame，使用全局主题配置确保样式统一。
    
    参数:
        parent: 父组件
        layout: 布局方向，Qt.Vertical 或 Qt.Horizontal，默认 Qt.Vertical
        margin: 边距，默认 0
        spacing: 间距，默认 2
        text_font: 文本字体，默认 "9pt 'Segoe UI'"
        enable_shadow: 是否启用阴影效果，默认 True
    
    示例:
        >>> frame = MangoFrame(parent, margin=10, spacing=5)
        >>> frame.layout.addWidget(MangoLabel("内容"))
    """

    def __init__(
            self,
            parent,
            layout=Qt.Vertical,  # type: ignore
            margin=0,
            spacing=2,
            text_font="9pt 'Segoe UI'",
            enable_shadow=True
    ):
        super().__init__()
        self.parent = parent
        self._layout_type = layout  # 保存布局类型参数，避免与 layout() 方法冲突
        self.margin = margin
        self.text_font = text_font
        self.enable_shadow = enable_shadow

        self.setObjectName("pod_bg_app")
        self.set_stylesheet()

        # 先检查是否有现有布局，如果有则复用；没有才创建新的布局
        existing_layout = super().layout()
        if existing_layout is None:
            # 创建新布局（不传入 widget，避免自动设置布局）
            if layout == Qt.Vertical:  # type: ignore
                self.layout = QHBoxLayout()
            else:
                self.layout = QHBoxLayout()
            self.layout.setContentsMargins(margin, margin, margin, margin)
            self.layout.setSpacing(spacing)
            # 设置新布局
            self.setLayout(self.layout)
        else:
            # 复用已存在的布局，避免重复 setLayout 产生 Qt 警告
            self.layout = existing_layout
            self.layout.setContentsMargins(margin, margin, margin, margin)
            self.layout.setSpacing(spacing)

        if enable_shadow:
            self.shadow = QGraphicsDropShadowEffect()
            self.shadow.setBlurRadius(20)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 160))
            self.setGraphicsEffect(self.shadow)

    def set_stylesheet(self, border_radius=None, border_size=None):
        """
        设置框架样式
        
        使用全局主题配置，确保样式统一。支持自定义边框圆角和边框大小。
        
        参数:
            border_radius: 自定义边框圆角颜色，如果为 None 则使用主题边框色
            border_size: 自定义边框大小，如果为 None 则使用默认值 1px
        """
        style = f"""
            #pod_bg_app {{
                background-color: {THEME.bg_100};
                border-radius: {THEME.border_radius};
                border: {border_size if border_size else '1'}px solid {border_radius if border_radius else THEME.bg_300};
            }}
            QFrame {{ 
                color: {THEME.text_100};
                font: {self.text_font};
            }}
            """
        self.setStyleSheet(style)
