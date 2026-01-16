# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 窗口调整手柄组件 - 提供统一的窗口调整手柄样式（用于调试和开发）
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoGrips(QWidget):
    """
    窗口调整手柄组件
    
    提供统一的窗口调整手柄样式，用于窗口大小调整。
    继承自 QWidget，支持8个方向的调整手柄（上、下、左、右、四个角）。
    主要用于调试和开发阶段，生产环境可通过 disable_color=True 隐藏颜色。
    
    参数:
        parent: 父窗口组件
        position: 手柄位置，可选值：
            - "top_left": 左上角
            - "top_right": 右上角
            - "bottom_left": 左下角
            - "bottom_right": 右下角
            - "top": 顶部
            - "bottom": 底部
            - "left": 左侧
            - "right": 右侧
        disable_color: 是否禁用颜色显示（设为透明），默认 True
    
    示例:
        >>> grip = MangoGrips(window, "bottom_right", disable_color=True)
    """
    def __init__(self, parent, position, disable_color=True):
        super().__init__()
        self.parent = parent
        self.setParent(parent)
        self.wi = Widgets()

        if position == "top_left":
            self.wi.top_left(self)
            grip = QSizeGrip(self.wi.top_left_grip)
            grip.setFixedSize(self.wi.top_left_grip.size())
            self.setGeometry(5, 5, 15, 15)

            if disable_color:
                self.wi.top_left_grip.setStyleSheet("background: transparent")

        if position == "top_right":
            self.wi.top_right(self)
            grip = QSizeGrip(self.wi.top_right_grip)
            grip.setFixedSize(self.wi.top_right_grip.size())
            self.setGeometry(self.parent.width() - 20, 5, 15, 15)

            if disable_color:
                self.wi.top_right_grip.setStyleSheet("background: transparent")

        if position == "bottom_left":
            self.wi.bottom_left(self)
            grip = QSizeGrip(self.wi.bottom_left_grip)
            grip.setFixedSize(self.wi.bottom_left_grip.size())
            self.setGeometry(5, self.parent.height() - 20, 15, 15)

            if disable_color:
                self.wi.bottom_left_grip.setStyleSheet("background: transparent")

        if position == "bottom_right":
            self.wi.bottom_right(self)
            grip = QSizeGrip(self.wi.bottom_right_grip)
            grip.setFixedSize(self.wi.bottom_right_grip.size())
            self.setGeometry(self.parent.width() - 20, self.parent.height() - 20, 15, 15)

            if disable_color:
                self.wi.bottom_right_grip.setStyleSheet("background: transparent")

        if position == "top":
            self.wi.top(self)
            self.setGeometry(0, 5, self.parent.width(), 10)
            self.setMaximumHeight(10)

            def resize_top(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(), self.parent.height() - delta.y())
                geo = self.parent.geometry()
                geo.setTop(geo.bottom() - height)
                self.parent.setGeometry(geo)
                event.accept()

            self.wi.top_grip.mouseMoveEvent = resize_top

            if disable_color:
                self.wi.top_grip.setStyleSheet("background: transparent")


        elif position == "bottom":
            self.wi.bottom(self)
            self.setGeometry(0, self.parent.height() - 10, self.parent.width(), 10)
            self.setMaximumHeight(10)

            def resize_bottom(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(), self.parent.height() + delta.y())
                self.parent.resize(self.parent.width(), height)
                event.accept()

            self.wi.bottom_grip.mouseMoveEvent = resize_bottom

            if disable_color:
                self.wi.bottom_grip.setStyleSheet("background: transparent")

        elif position == "left":
            self.wi.left(self)
            self.setGeometry(0, 10, 10, self.parent.height())
            self.setMaximumWidth(10)

            def resize_left(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(), self.parent.width() - delta.x())
                geo = self.parent.geometry()
                geo.setLeft(geo.right() - width)
                self.parent.setGeometry(geo)
                event.accept()

            self.wi.left_grip.mouseMoveEvent = resize_left

            if disable_color:
                self.wi.left_grip.setStyleSheet("background: transparent")


        elif position == "right":
            self.wi.right(self)
            self.setGeometry(self.parent.width() - 10, 10, 10, self.parent.height())
            self.setMaximumWidth(10)

            def resize_right(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(), self.parent.width() + delta.x())
                self.parent.resize(width, self.parent.height())
                event.accept()

            self.wi.right_grip.mouseMoveEvent = resize_right

            if disable_color:
                self.wi.right_grip.setStyleSheet("background: transparent")

    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件
        
        参数:
            event: 鼠标释放事件对象
        """
        self.mousePos = None

    def resizeEvent(self, event):
        """
        窗口大小调整事件
        
        当窗口大小改变时，更新手柄的位置和大小。
        
        参数:
            event: 大小调整事件对象
        """
        if hasattr(self.wi, 'top_grip'):
            self.wi.top_grip.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, 'bottom_grip'):
            self.wi.bottom_grip.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, 'left_grip'):
            self.wi.left_grip.setGeometry(0, 0, 10, self.height() - 20)

        elif hasattr(self.wi, 'right_grip'):
            self.wi.right_grip.setGeometry(0, 0, 10, self.height() - 20)

        elif hasattr(self.wi, 'top_right_grip'):
            self.wi.top_right_grip.setGeometry(self.width() - 15, 0, 15, 15)

        elif hasattr(self.wi, 'bottom_left_grip'):
            self.wi.bottom_left_grip.setGeometry(0, self.height() - 15, 15, 15)

        elif hasattr(self.wi, 'bottom_right_grip'):
            self.wi.bottom_right_grip.setGeometry(self.width() - 15, self.height() - 15, 15, 15)


class Widgets:
    """
    手柄内部组件类
    
    用于创建和配置不同位置的手柄组件。
    使用主题颜色确保样式统一，但保留调试用的高对比度颜色以便区分方向。
    """
    def top_left(self, form):
        """
        创建左上角手柄
        
        参数:
            form: 父组件
        """
        self.top_left_grip = QFrame(form)
        self.top_left_grip.setObjectName(u"top_left_grip")
        self.top_left_grip.setFixedSize(15, 15)
        # 使用主题颜色，但保留边框以便调试时区分
        self.top_left_grip.setStyleSheet(f"background-color: {THEME.bg_300}; border: 2px solid {THEME.primary_100};")

    def top_right(self, form):
        """
        创建右上角手柄
        
        参数:
            form: 父组件
        """
        self.top_right_grip = QFrame(form)
        self.top_right_grip.setObjectName(u"top_right_grip")
        self.top_right_grip.setFixedSize(15, 15)
        self.top_right_grip.setStyleSheet(f"background-color: {THEME.bg_300}; border: 2px solid {THEME.primary_100};")

    def bottom_left(self, form):
        """
        创建左下角手柄
        
        参数:
            form: 父组件
        """
        self.bottom_left_grip = QFrame(form)
        self.bottom_left_grip.setObjectName(u"bottom_left_grip")
        self.bottom_left_grip.setFixedSize(15, 15)
        self.bottom_left_grip.setStyleSheet(f"background-color: {THEME.bg_300}; border: 2px solid {THEME.primary_100};")

    def bottom_right(self, form):
        """
        创建右下角手柄
        
        参数:
            form: 父组件
        """
        self.bottom_right_grip = QFrame(form)
        self.bottom_right_grip.setObjectName(u"bottom_right_grip")
        self.bottom_right_grip.setFixedSize(15, 15)
        self.bottom_right_grip.setStyleSheet(f"background-color: {THEME.bg_300}; border: 2px solid {THEME.primary_100};")

    def top(self, form):
        """
        创建顶部手柄
        
        参数:
            form: 父组件
        """
        self.top_grip = QFrame(form)
        self.top_grip.setObjectName(u"top_grip")
        self.top_grip.setGeometry(QRect(0, 0, 500, 10))
        # 使用主题颜色
        self.top_grip.setStyleSheet(f"background-color: {THEME.accent_200};")
        self.top_grip.setCursor(QCursor(Qt.SizeVerCursor))  # type: ignore

    def bottom(self, form):
        """
        创建底部手柄
        
        参数:
            form: 父组件
        """
        self.bottom_grip = QFrame(form)
        self.bottom_grip.setObjectName(u"bottom_grip")
        self.bottom_grip.setGeometry(QRect(0, 0, 500, 10))
        # 使用主题颜色
        self.bottom_grip.setStyleSheet(f"background-color: {THEME.accent_200};")
        self.bottom_grip.setCursor(QCursor(Qt.SizeVerCursor))  # type: ignore

    def left(self, form):
        """
        创建左侧手柄
        
        参数:
            form: 父组件
        """
        self.left_grip = QFrame(form)
        self.left_grip.setObjectName(u"left")
        self.left_grip.setGeometry(QRect(0, 10, 10, 480))
        self.left_grip.setMinimumSize(QSize(10, 0))
        self.left_grip.setCursor(QCursor(Qt.SizeHorCursor))  # type: ignore
        # 使用主题颜色
        self.left_grip.setStyleSheet(f"background-color: {THEME.accent_200};")

    def right(self, form):
        """
        创建右侧手柄
        
        参数:
            form: 父组件
        """
        self.right_grip = QFrame(form)
        self.right_grip.setObjectName(u"right")
        self.right_grip.setGeometry(QRect(0, 0, 10, 500))
        self.right_grip.setMinimumSize(QSize(10, 0))
        self.right_grip.setCursor(QCursor(Qt.SizeHorCursor))  # type: ignore
        # 使用主题颜色
        self.right_grip.setStyleSheet(f"background-color: {THEME.accent_200};")
