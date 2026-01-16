# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: main_2 专用标题栏按钮（与菜单同底色，无 tooltip）
# @Time   : 2025-01-14
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.settings.settings import THEME


class MangoTitleButtonMain2(QPushButton):
    """
    main_2 专用标题栏按钮

    - 底色与左侧菜单背景一致（THEME.bg_300）
    - 悬停/按下只变图标颜色，不改变底色
    - 默认不显示 tooltip
    """

    def __init__(
            self,
            parent,
            app_parent=None,
            tooltip_text="",
            btn_id=None,
            icon_path="",
            is_active=False
    ):
        super().__init__()
        self.url = None
        self.setFixedSize(30, 30)
        self.setCursor(Qt.PointingHandCursor)  # type: ignore
        self.setObjectName(btn_id)

        # main_2 配色：底色与菜单一致
        self._context_color = THEME.bg_300
        self.text_foreground = THEME.text_200
        self._set_bg_color = THEME.bg_300
        self._set_icon_color = THEME.text_100

        self._top_margin = self.height() + 6
        self._is_active = is_active
        self._set_icon_path = icon_path
        self._parent = parent
        self._app_parent = app_parent

        # main_2 不需要 tooltip，若传入空字符串则不创建
        self._tooltip_text = tooltip_text
        self._tooltip: _ToolTip | None = None
        if tooltip_text:
            self._tooltip = _ToolTip(
                app_parent,
                tooltip_text,
                THEME.bg_100,
                THEME.bg_300,
                self.text_foreground
            )
            self._tooltip.hide()

    def set_active(self, is_active):
        self._is_active = is_active
        self.repaint()

    def is_active(self):
        return self._is_active

    def paintEvent(self, event):
        paint = QPainter()
        if not paint.begin(self):
            return
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 底色保持与菜单一致
        brush = QBrush(QColor(self._set_bg_color))
        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.NoPen)  # type: ignore
        paint.setBrush(brush)
        paint.drawRoundedRect(rect, 8, 8)
        self.icon_paint(paint, self._set_icon_path, rect)
        paint.end()

    def change_style(self, event):
        if event == QEvent.Enter:  # type: ignore
            self._set_bg_color = THEME.bg_300
            self._set_icon_color = THEME.text_200
            self.repaint()
        elif event == QEvent.Leave:  # type: ignore
            self._set_bg_color = THEME.bg_300
            self._set_icon_color = THEME.text_100
            self.repaint()
        elif event == QEvent.MouseButtonPress:  # type: ignore
            self._set_bg_color = THEME.bg_300
            self._set_icon_color = THEME.text_100
            self.repaint()
        elif event == QEvent.MouseButtonRelease:  # type: ignore
            self._set_bg_color = THEME.bg_300
            self._set_icon_color = THEME.text_100
            self.repaint()

    def enterEvent(self, event):
        self.change_style(QEvent.Enter)  # type: ignore
        if self._tooltip is not None:
            self.move_tooltip()
            self._tooltip.show()

    def leaveEvent(self, event):
        self.change_style(QEvent.Leave)  # type: ignore
        if self._tooltip is not None:
            self.move_tooltip()
            self._tooltip.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # type: ignore
            self.change_style(QEvent.MouseButtonPress)  # type: ignore
            self.setFocus()
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:  # type: ignore
            self.change_style(QEvent.MouseButtonRelease)  # type: ignore
            return self.released.emit()

    def icon_paint(self, qp, image, rect):
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
        self._set_icon_path = icon_path
        self.repaint()

    def move_tooltip(self):
        if self._tooltip is None:
            return
        gp = self.mapToGlobal(QPoint(0, 0))
        pos = self._parent.mapFromGlobal(gp)
        pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        pos_y = pos.y() + self._top_margin
        self._tooltip.move(pos_x, pos_y)


class _ToolTip(QLabel):
    def __init__(
            self,
            parent,
            tooltip,
            dark_one,
            context_color,
            text_foreground
    ):
        QLabel.__init__(self)

        style = f"""
            QLabel#label_tooltip {{ 
                background-color: {dark_one};
                color: {text_foreground};
                padding: 6px 12px; 
                border-radius: {THEME.border_radius}; 
                border: 1px solid {context_color}; 
                font-family: {THEME.font.family}; 
                font-size: {THEME.font.text_size}px; 
                font-weight: 500;
            }}
        """
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
