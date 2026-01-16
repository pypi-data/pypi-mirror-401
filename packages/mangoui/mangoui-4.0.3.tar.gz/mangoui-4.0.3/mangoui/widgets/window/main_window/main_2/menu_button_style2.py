# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 菜单按钮样式2 - 完全扁平化的现代化菜单按钮样式
# @Time   : 2025-01-14
# @Author : 毛鹏

from PySide6.QtCore import QRect, QPoint, Signal
from PySide6.QtGui import QColor, Qt, QPainter, QPixmap, QFont
from PySide6.QtWidgets import QLabel, QWidget

from mangoui.settings.settings import THEME


class MangoMenuButtonStyle2(QWidget):
    """
    main_2 左侧菜单按钮（正方形）：图标在上，文字在下，悬停和选中样式一致
    """

    # 保持与 QPushButton 类似的信号接口
    clicked = Signal()
    released = Signal()

    def __init__(
            self,
            app_parent,
            text,
            tooltip_text='',
            url=None,
            btn_id=None,
            icon_path=None,
            is_active=False,
            height=68,
    ):
        super().__init__()
        # 文本交给自绘
        self._text = text

        self.url = url
        self.setCursor(Qt.PointingHandCursor)  # type: ignore
        self.setFixedSize(height, height)      # 正方形按钮
        self.setObjectName(btn_id)

        self._icon_path = icon_path
        self._icon_size = 24
        self._is_active = is_active
        self._is_hovered = False

        self.app_parent = app_parent
        # main_2 不需要 tooltip，保留属性但不使用
        self.tooltip_text = ""

        self._update_style()

    def _update_style(self):
        """基础 QSS，仅设置字体等，不做配色"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
                border: none;
                border-radius: 0px;
                padding: 0px;
                margin: 0px;
                text-align: center;
                font-family: {THEME.font.family};
                font-size: {THEME.font.text_size - 1}px;
            }}
            QWidget:hover {{
                padding: 0px;
                margin: 0px;
            }}
            QWidget:pressed {{
                padding: 0px;
                margin: 0px;
            }}
        """)

    def paintEvent(self, event):
        """自定义绘制：正方形背景 + 图标 + 文字"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 使用固定的 rect，不受按钮状态影响
        rect = QRect(0, 0, self.width(), self.height())

        # 背景：悬停和选中同一种深一点的颜色
        if self._is_active or self._is_hovered:
            bg_color = QColor(THEME.bg_300)
        else:
            bg_color = Qt.transparent  # type: ignore
        painter.fillRect(rect, bg_color)

        # 固定的边距，确保位置不变
        top_margin = 10
        bottom_margin = 8
        button_width = self.width()
        button_height = self.height()

        # 图标居中绘制 - 使用固定坐标计算
        if self._icon_path:
            icon_x = (button_width - self._icon_size) // 2
            icon_y = top_margin

            pixmap = QPixmap(self._icon_path)
            if not pixmap.isNull():
                # 悬停时仅底色变化，图标颜色只跟激活状态有关
                icon_color = QColor(THEME.primary_100) if self._is_active else QColor(THEME.text_200)
                pixmap = self._tint_pixmap(pixmap, icon_color)
                # 使用固定的整数坐标，避免像素偏移
                painter.drawPixmap(int(icon_x), int(icon_y), self._icon_size, self._icon_size, pixmap)

        # 文字在图标下方，水平居中 - 使用固定坐标
        text_top = top_margin + self._icon_size + 4
        text_rect = QRect(
            0,
            int(text_top),
            button_width,
            int(button_height - text_top - bottom_margin),
        )
        font = QFont(THEME.font.family, THEME.font.text_size - 1)
        painter.setFont(font)
        # 悬停时仅底色变化，文字颜色只跟激活状态有关
        text_color = QColor(THEME.primary_100) if self._is_active else QColor(THEME.text_200)
        painter.setPen(text_color)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self._text)  # type: ignore

    def _tint_pixmap(self, pixmap: QPixmap, color: QColor) -> QPixmap:
        """为图标着色"""
        tinted = QPixmap(pixmap.size())
        tinted.fill(Qt.transparent)  # type: ignore
        
        painter = QPainter(tinted)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(tinted.rect(), color)
        painter.end()
        
        return tinted

    def mousePressEvent(self, event):
        """鼠标按下事件：只做点击标记，不改变布局"""
        if event.button() == Qt.LeftButton:  # type: ignore
            self.clicked.emit()
            self.update()
        QWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        """鼠标释放事件：不改变布局"""
        if event.button() == Qt.LeftButton:  # type: ignore
            self.released.emit()
            self.update()
        QWidget.mouseReleaseEvent(self, event)

    def enterEvent(self, event):
        """鼠标进入事件：仅改变 hover 状态"""
        self._is_hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开事件：取消 hover 状态"""
        self._is_hovered = False
        self.update()
        super().leaveEvent(event)

    def set_active(self, is_active: bool):
        """
        设置激活状态
        
        参数:
            is_active: 是否激活
        """
        self._is_active = is_active
        self._update_style()
        self.update()  # 触发重绘

    def is_active(self) -> bool:
        """获取激活状态"""
        return self._is_active


class _ToolTip(QLabel):
    """工具提示组件（目前 main_2 未启用，保留以兼容旧逻辑）"""
    def __init__(self, parent, text, bg_color, text_color, border_color):
        super().__init__(parent)
        self.setText(text)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: {THEME.border_radius};
                padding: 5px 10px;
            }}
        """)
        self.hide()

    def show_tooltip(self, button):
        """显示工具提示"""
        if not self.text():
            return

        button_pos = button.mapToGlobal(QPoint(0, 0))
        self.move(button_pos.x() + button.width() + 10, button_pos.y())
        self.show()
