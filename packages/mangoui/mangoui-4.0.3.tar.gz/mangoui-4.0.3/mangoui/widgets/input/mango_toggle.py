# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 开关组件 - 提供统一的开关切换样式和动画效果
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.enums.enums import StatusEnum
from mangoui.models.models import ComboBoxDataModel
from mangoui.settings.settings import THEME


class MangoToggle(QCheckBox):
    """
    开关组件
    
    提供统一的开关切换样式，支持平滑的动画过渡效果。
    继承自 QCheckBox，使用全局主题配置确保样式统一。
    通过自定义绘制和属性动画实现现代化的开关效果。
    
    信号:
        click: 当开关被点击时触发，传递包含值的字典
        change_requested: 当开关状态改变请求时触发
    
    参数:
        value: 初始值，True 表示开启，False 表示关闭
        auto_update_status: 是否自动更新状态，默认 True
        **kwargs: 额外参数
    
    示例:
        >>> toggle = MangoToggle(value=True)
        >>> toggle.click.connect(lambda v: print(f"开关状态: {v}"))
    """
    click = Signal(object)
    change_requested = Signal(object)

    def __init__(self, value=False, auto_update_status=True, **kwargs):
        super().__init__()
        self.value = value
        self.kwargs = kwargs
        self.auto_update_status = auto_update_status
        self.data = [ComboBoxDataModel(id=str(i.get('id')), name=i.get('name')) for i in [
            {'id': 0, 'name': '关闭&进行中&失败'}, {'id': 1, 'name': '启用&已完成&通过'}]]
        self.setFixedSize(50, 28)
        self.setCursor(Qt.PointingHandCursor)  # type: ignore

        self._position = 3
        self.animation = QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(QEasingCurve.OutBounce)  # type: ignore
        self.animation.setDuration(500)
        self.clicked.connect(self.on_clicked)
        self.stateChanged.connect(self.set_animation)
        self.set_value(self.value)
        self.change_requested.connect(self.set_animation)

    def get_value(self) -> int:
        """
        获取开关的值
        
        返回:
            int: 0 表示关闭，1 表示开启
        """
        return int(self.isChecked())

    def set_value(self, value: bool | StatusEnum):
        """
        设置开关的值
        
        参数:
            value: 开关的值，可以是 bool 或 StatusEnum
        """
        if value is None:
            return
        if isinstance(value, StatusEnum):
            self.value = bool(value)
        else:
            self.value = value
        self.setChecked(self.value)

    @Property(float)
    def position(self):
        """
        获取滑块位置属性
        
        用于动画控制滑块的当前位置。
        """
        return self._position

    @position.setter
    def position(self, pos):
        """
        设置滑块位置属性
        
        参数:
            pos: 滑块位置（像素值）
        """
        self._position = pos
        self.update()

    def on_clicked(self, value):
        """
        点击事件处理
        
        当开关被点击时调用，根据 auto_update_status 决定是否自动更新状态。
        
        参数:
            value: 点击后的值
        """
        if self.auto_update_status:
            self.set_value(value)
        self.click.emit({'value': int(self.isChecked())})

    def set_animation(self, value):
        """
        设置动画效果
        
        根据开关状态设置滑块动画的结束位置，实现平滑的切换效果。
        
        参数:
            value: 开关状态值
        """
        self.animation.stop()
        if self.isChecked():
            self.animation.setEndValue(self.width() - 27)
        else:
            self.animation.setEndValue(3)
        self.animation.start()

    def hitButton(self, pos: QPoint):
        """
        判断点击位置是否在按钮范围内
        
        参数:
            pos: 点击位置
        
        返回:
            bool: True 表示在范围内，False 表示不在范围内
        """
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        """
        自定义绘制事件
        
        绘制开关的背景和滑块，根据开关状态使用不同的颜色。
        开启状态使用主题主色，关闭状态使用背景色和强调色。
        
        参数:
            e: 绘制事件对象
        """
        p = QPainter(self)
        if not p.isActive():
            return
        p.setRenderHint(QPainter.Antialiasing)  # type: ignore
        p.setFont(QFont(THEME.font.family, THEME.font.text_size))
        p.setPen(Qt.NoPen)  # type: ignore
        
        # 获取组件尺寸
        rect = QRect(0, 0, self.width(), self.height())
        
        # 绘制带边框的背景
        if self.isChecked():
            # 开启状态
            p.setBrush(QColor(THEME.primary_100))
            p.setPen(QPen(QColor(THEME.primary_100), 1))  # 添加边框
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            # 绘制滑块（开启状态）
            p.setBrush(QColor(THEME.bg_100))
            p.setPen(Qt.NoPen)  # 滑块无边框
            p.drawEllipse(self._position, 3, 22, 22)
        else:
            # 关闭状态
            p.setBrush(QColor(THEME.bg_200))
            p.setPen(QPen(QColor(THEME.accent_100), 1))  # 添加边框
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            # 绘制滑块（关闭状态）
            p.setBrush(QColor(THEME.accent_200))
            p.setPen(Qt.NoPen)  # 滑块无边框
            p.drawEllipse(self._position, 3, 22, 22)
        
        # 移除文字绘制部分
        
        p.end()