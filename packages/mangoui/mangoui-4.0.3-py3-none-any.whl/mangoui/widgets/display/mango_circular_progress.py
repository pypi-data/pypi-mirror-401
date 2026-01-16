# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 圆形进度条组件 - 提供统一的圆形进度条样式和自定义绘制
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏
from PySide6.QtCore import QRect
from PySide6.QtGui import QColor, QPainter, QFont, Qt, QPen
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect

from mangoui.settings.settings import THEME


class MangoCircularProgress(QWidget):
    """
    圆形进度条组件
    
    提供统一的圆形进度条样式，支持自定义颜色、文本显示和阴影效果。
    继承自 QWidget，通过自定义绘制实现圆形进度显示。
    
    参数:
        parent: 父组件
        value: 当前进度值，默认 0
        progress_width: 进度条宽度，默认 10px
        is_rounded: 是否使用圆角端点，默认 True
        max_value: 最大值，默认 100
        progress_color: 进度条颜色，默认使用主题次要主色
        enable_text: 是否显示文本，默认 True
        font_family: 字体族，默认 "微软雅黑"
        font_size: 字体大小，默认 12px
        suffix: 文本后缀，默认 "%"
        text_color: 文本颜色，默认使用主题主要文本色
        enable_bg: 是否显示背景圆环，默认 True
        bg_color: 背景圆环颜色，默认使用主题背景主色
        *args, **kwargs: 额外参数
    
    示例:
        >>> circular = MangoCircularProgress(parent, value=50, max_value=100)
        >>> circular.set_value(75)
    """
    def __init__(self,
                 parent,
                 value=0,
                 progress_width=10,
                 is_rounded=True,
                 max_value=100,
                 progress_color=THEME.primary_200,
                 enable_text=True,
                 font_family="微软雅黑",
                 font_size=12,
                 suffix="%",
                 text_color=THEME.text_100,
                 enable_bg=True,
                 bg_color=THEME.primary_300,
                 *args,
                 **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.value = value
        self.progress_width = progress_width
        self.progress_rounded_cap = is_rounded
        self.max_value = max_value
        self.progress_color = progress_color
        self.enable_text = enable_text
        self.font_family = font_family
        self.font_size = font_size
        self.suffix = suffix
        self.text_color = text_color
        self.enable_bg = enable_bg
        self.bg_color = bg_color

    def add_shadow(self, enable):
        """
        添加阴影效果
        
        参数:
            enable: bool，True 表示启用阴影，False 表示禁用阴影
        """
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 80))
            self.setGraphicsEffect(self.shadow)

    def set_value(self, value):
        """
        设置进度值
        
        参数:
            value: 新的进度值
        """
        self.value = value
        self.repaint()

    def paintEvent(self, e):
        """
        自定义绘制事件
        
        绘制背景圆环、进度圆环和中心文本。
        
        参数:
            e: 绘制事件对象
        """
        width = self.width() - self.progress_width
        height = self.height() - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        paint = QPainter()
        if not paint.begin(self):
            return
        paint.setRenderHint(QPainter.Antialiasing)  # type: ignore
        paint.setFont(QFont(self.font_family, self.font_size))

        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.NoPen)  # type: ignore

        # 绘制背景圆环
        if self.enable_bg:
            pen = QPen()
            pen.setWidth(self.progress_width)
            pen.setColor(QColor(self.bg_color))
            if self.progress_rounded_cap:
                pen.setCapStyle(Qt.RoundCap)  # type: ignore
            paint.setPen(pen)
            paint.drawArc(int(margin), int(margin), int(width), int(height), 0, 360 * 16)  # type: ignore

        # 绘制进度圆环
        pen = QPen()
        pen.setWidth(self.progress_width)
        pen.setColor(QColor(self.progress_color))
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)  # type: ignore
        paint.setPen(pen)
        paint.drawArc(int(margin), int(margin), int(width), int(height), -90 * 16, -int(value * 16))  # type: ignore

        # 绘制中心文本
        if self.enable_text:
            # 添加阴影效果
            text_rect = QRect(int(margin), int(margin), int(width), int(height))
            # 绘制阴影
            shadow_pen = QPen()
            shadow_pen.setColor(QColor(0, 0, 0, 30))  # 半透明黑色阴影
            paint.setPen(shadow_pen)
            paint.drawText(text_rect, Qt.AlignCenter, f"{self.value}{self.suffix}")  # type: ignore
            
            # 绘制主文本
            pen.setColor(QColor(self.text_color))
            paint.setPen(pen)
            paint.drawText(rect, Qt.AlignCenter, f"{self.value}{self.suffix}")  # type: ignore

        paint.end()
