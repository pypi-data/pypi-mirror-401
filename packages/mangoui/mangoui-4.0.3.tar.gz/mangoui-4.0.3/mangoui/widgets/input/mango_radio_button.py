# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 单选按钮组件 - 提供统一的单选按钮样式和交互效果
# @Time   : 2025-11-25 10:10
# @Author : Qwen

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from mangoui.settings.settings import THEME


class MangoRadioButton(QRadioButton):
    """
    单选按钮组件
    
    提供统一的单选按钮样式，支持选中、悬停、禁用等状态。
    继承自 QRadioButton，使用全局主题配置确保样式统一。
    通过自定义 paintEvent 实现内部圆点的精确居中显示。
    
    参数:
        text: 单选按钮显示的文本标签
        parent: 父组件
        **kwargs: 额外参数
    
    示例:
        >>> radio1 = MangoRadioButton("选项1")
        >>> radio2 = MangoRadioButton("选项2")
        >>> radio1.setChecked(True)
    """
    def __init__(self, text="", parent=None, **kwargs):
        super().__init__(text, parent)
        self.kwargs = kwargs
        self.set_stylesheet()
        
    def set_stylesheet(self):
        """
        设置单选按钮样式
        
        使用全局主题配置，确保样式统一。包括正常状态、悬停状态、选中状态和禁用状态的样式。
        """
        style = f"""
        QRadioButton {{
            spacing: 8px;
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}

        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 9px;
        }}

        QRadioButton::indicator:unchecked {{
            border: 1px solid {THEME.bg_300};
            background-color: {THEME.bg_100};
        }}

        QRadioButton::indicator:unchecked:hover {{
            border: 1px solid {THEME.primary_100};
        }}

        QRadioButton::indicator:unchecked:pressed {{
            border: 1px solid {THEME.primary_200};
            background-color: {THEME.bg_200};
        }}

        QRadioButton::indicator:checked {{
            border: 1px solid {THEME.primary_100};
            background-color: {THEME.bg_100};
        }}

        QRadioButton::indicator:checked:hover {{
            border: 1px solid {THEME.primary_200};
        }}

        QRadioButton::indicator:checked:pressed {{
            border: 1px solid {THEME.primary_100};
        }}

        QRadioButton:disabled {{
            color: {THEME.text_200};
        }}

        QRadioButton::indicator:disabled {{
            border: 1px solid {THEME.bg_200};
            background-color: {THEME.bg_200};
        }}

        QRadioButton::indicator:checked:disabled {{
            border: 1px solid {THEME.bg_300};
            background-color: {THEME.bg_200};
        }}
        """
        self.setStyleSheet(style)
        self.setMinimumHeight(30)
    
    def paintEvent(self, event):
        """
        自定义绘制事件
        
        实现内部圆点的精确居中显示。当按钮处于选中状态时，在指示器中心绘制一个圆点。
        圆点颜色根据按钮状态（正常、悬停、禁用）动态变化。
        
        参数:
            event: 绘制事件对象
        """
        super().paintEvent(event)
        
        if not self.isChecked():
            return
        
        # 获取 indicator 的位置和大小
        option = QStyleOptionButton()
        self.initStyleOption(option)
        style = self.style()
        indicator_rect = style.subElementRect(QStyle.SE_RadioButtonIndicator, option, self)
        
        if not indicator_rect.isValid():
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        
        # 根据状态选择颜色
        if not self.isEnabled():
            dot_color = QColor(THEME.text_200)
        elif option.state & QStyle.State_MouseOver:
            dot_color = QColor(THEME.primary_200)
        else:
            dot_color = QColor(THEME.primary_100)
        
        # 绘制内部圆点（直径为 10px，精确居中）
        # indicator 尺寸为 18x18，圆点直径为 10px，半径为 5px
        dot_radius = 5
        
        # 使用 QRectF 转换 indicator_rect 以获得精确的浮点数坐标
        indicator_rect_f = QRectF(indicator_rect)
        center = indicator_rect_f.center()
        
        # 绘制圆点，使用 QRectF 确保精确绘制
        dot_rect = QRectF(center.x() - dot_radius, center.y() - dot_radius, 
                         dot_radius * 2, dot_radius * 2)
        painter.setBrush(dot_color)
        painter.drawEllipse(dot_rect)