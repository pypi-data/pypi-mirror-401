# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 图标按钮组件 - 提供统一的图标按钮样式和工具提示功能
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoIconButton(QPushButton):
    """
    图标按钮组件
    
    提供统一的图标按钮样式，支持自定义图标、工具提示和激活状态。
    继承自 QPushButton，使用全局主题配置确保样式统一。
    通过自定义绘制实现图标颜色变化和悬停效果。
    
    参数:
        parent: 父组件
        app_parent: 应用程序父组件，用于工具提示定位
        icon_path: 图标路径，默认使用心形图标
        tooltip_text: 工具提示文本
        btn_id: 按钮ID，用于对象标识
    
    示例:
        >>> icon_btn = MangoIconButton(parent, app_parent, ":/icons/settings.svg", "设置")
        >>> icon_btn.set_active(True)
    """
    def __init__(
            self,
            parent,
            app_parent,
            icon_path=":/icons/icon_heart.svg",
            tooltip_text="",
            btn_id=None
    ):
        super().__init__()
        self.parent = parent
        self.setObjectName(btn_id)
        self.app_parent = app_parent
        self.tooltip_text = tooltip_text

        self.setFixedSize(30, 30)
        self.setCursor(Qt.PointingHandCursor)  # type: ignore

        # 使用主题颜色，确保样式统一
        self._context_color = THEME.primary_100
        self.text_foreground = THEME.text_200
        self._set_bg_color = THEME.bg_100

        self._top_margin = 40
        self._is_active = False
        self._set_icon_path = icon_path
        self._set_icon_color = THEME.primary_100

        self.tooltip = _ToolTip(
            app_parent,
            tooltip_text,
            THEME.bg_300,
            self.text_foreground
        )
        self.tooltip.hide()

    def set_active(self, is_active):
        """
        设置按钮激活状态
        
        参数:
            is_active: bool，True 表示激活状态，False 表示非激活状态
        """
        self._is_active = is_active
        self.repaint()

    def is_active(self):
        """
        获取按钮激活状态
        
        返回:
            bool: True 表示激活状态，False 表示非激活状态
        """
        return self._is_active

    def paintEvent(self, event):
        """
        自定义绘制事件
        
        绘制按钮背景和图标，根据激活状态使用不同的颜色。
        
        参数:
            event: 绘制事件对象
        """
        paint = QPainter()
        if not paint.begin(self):
            return
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._is_active:
            brush = QBrush(QColor(self._context_color))
        else:
            brush = QBrush(QColor(self._set_bg_color))

        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.NoPen)  # type: ignore
        paint.setBrush(brush)
        paint.drawRoundedRect(
            rect,
            THEME.border_radius,
            THEME.border_radius
        )

        self.icon_paint(paint, self._set_icon_path, rect)

        paint.end()

    def change_style(self, event):
        """
        根据事件改变按钮样式
        
        根据鼠标进入、离开、按下、释放等事件改变背景色和图标颜色。
        
        参数:
            event: 事件类型（Enter、Leave、MouseButtonPress、MouseButtonRelease）
        """
        if event == QEvent.Enter:  # type: ignore
            self._set_bg_color = THEME.primary_200
            self._set_icon_color = THEME.primary_200
            self.repaint()
        elif event == QEvent.Leave:  # type: ignore
            self._set_bg_color = THEME.bg_100
            self._set_icon_color = THEME.primary_100
            self.repaint()
        elif event == QEvent.MouseButtonPress:  # type: ignore
            self._set_bg_color = THEME.primary_300
            self._set_icon_color = THEME.primary_100
            self.repaint()
        elif event == QEvent.MouseButtonRelease:  # type: ignore
            self._set_bg_color = THEME.bg_100
            self._set_icon_color = THEME.primary_200
            self.repaint()

    def enterEvent(self, event):
        """
        鼠标进入事件
        
        当鼠标进入按钮区域时，改变样式并显示工具提示。
        
        参数:
            event: 鼠标进入事件对象
        """
        self.change_style(QEvent.Enter)  # type: ignore
        self.move_tooltip()
        self.tooltip.show()

    def leaveEvent(self, event):
        """
        鼠标离开事件
        
        当鼠标离开按钮区域时，改变样式并隐藏工具提示。
        
        参数:
            event: 鼠标离开事件对象
        """
        self.change_style(QEvent.Leave)  # type: ignore
        self.move_tooltip()
        self.tooltip.hide()

    def mousePressEvent(self, event):
        """
        鼠标按下事件
        
        当鼠标按下时，改变样式并触发点击信号。
        
        参数:
            event: 鼠标按下事件对象
        """
        if event.button() == Qt.LeftButton:  # type: ignore
            self.change_style(QEvent.MouseButtonPress)  # type: ignore
            self.setFocus()
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件
        
        当鼠标释放时，改变样式并触发释放信号。
        
        参数:
            event: 鼠标释放事件对象
        """
        if event.button() == Qt.LeftButton:  # type: ignore
            self.change_style(QEvent.MouseButtonRelease)  # type: ignore
            return self.released.emit()

    def icon_paint(self, qp, image, rect):
        """
        绘制图标
        
        根据激活状态绘制不同颜色的图标。
        
        参数:
            qp: QPainter 对象
            image: 图标路径
            rect: 绘制区域
        """
        if not image:
            return
        icon = QPixmap(image)
        if icon.isNull():
            return
        painter = QPainter(icon)
        if not painter.isActive():
            return
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)  # type: ignore
        if self._is_active:
            painter.fillRect(icon.rect(), THEME.primary_100)
        else:
            painter.fillRect(icon.rect(), self._set_icon_color)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon
        )
        painter.end()

    def set_icon(self, icon_path):
        """
        设置图标路径
        
        参数:
            icon_path: 新的图标路径
        """
        self._set_icon_path = icon_path
        self.repaint()

    def move_tooltip(self):
        """
        移动工具提示位置
        
        根据按钮位置计算工具提示的显示位置，使其居中显示在按钮上方。
        """
        gp = self.mapToGlobal(QPoint(0, 0))

        pos = self.parent.mapFromGlobal(gp)

        pos_x = (pos.x() - (self.tooltip.width() // 2)) + (self.width() // 2)
        pos_y = pos.y() - self._top_margin

        self.tooltip.move(pos_x, pos_y)


class _ToolTip(QLabel):
    """
    工具提示内部类
    
    用于显示图标按钮的工具提示，使用统一的样式和阴影效果。
    """
    style_tooltip = """ 
    QLabel {{		
        background-color: {_dark_one};	
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        font-family: {THEME.font.family};
        font-size: 9pt;
        font-weight: 800;
    }}
    """

    def __init__(
            self,
            parent,
            tooltip,
            dark_one,
            text_foreground
    ):
        """
        初始化工具提示
        
        参数:
            parent: 父组件
            tooltip: 工具提示文本
            dark_one: 背景颜色
            text_foreground: 文本颜色
        """
        QLabel.__init__(self)

        style = self.style_tooltip.format(
            _dark_one=dark_one,
            _text_foreground=text_foreground
        )
        self.setObjectName(u"label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
