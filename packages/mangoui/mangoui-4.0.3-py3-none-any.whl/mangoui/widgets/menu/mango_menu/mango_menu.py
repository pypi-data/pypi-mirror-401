# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 菜单组件 - 提供统一的侧边菜单样式和展开/折叠动画效果
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏


from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.models.models import LeftMenuModel
from mangoui.settings.settings import THEME
from .mango_div import MangoDiv
from .mango_menu_button import MangoMenuButton


class MangoMenu(QWidget):
    """
    菜单组件
    
    提供统一的侧边菜单样式，支持展开/折叠动画和菜单项管理。
    继承自 QWidget，使用全局主题配置确保样式统一。
    
    信号:
        clicked: 当菜单项被点击时触发，传递菜单模型
        released: 当菜单项被释放时触发，传递菜单模型
    
    参数:
        parent: 父组件
        app_parent: 应用程序父组件
        duration_time: 动画持续时间（毫秒），默认 500
        minimum_width: 最小宽度，默认 50
        maximum_width: 最大宽度，默认 180
        icon_path: 展开图标路径，默认使用菜单图标
        icon_path_close: 折叠图标路径，默认使用关闭菜单图标
        toggle_text: 切换按钮文本，默认 "展开"
        toggle_tooltip: 切换按钮工具提示，默认 "展开菜单"
    
    示例:
        >>> menu = MangoMenu(parent, app_parent)
        >>> menu.add_menus([LeftMenuModel(...)])
    """
    clicked = Signal(LeftMenuModel)
    released = Signal(LeftMenuModel)

    def __init__(
            self,
            parent=None,
            app_parent=None,
            duration_time=500,
            minimum_width=50,
            maximum_width=180,
            icon_path=":/icons/menu.svg",
            icon_path_close=":/icons/icon_menu_close.svg",
            toggle_text="展开",
            toggle_tooltip="展开菜单"
    ):
        super().__init__()
        self.duration_time = duration_time
        self.minimum_width = minimum_width
        self.maximum_width = maximum_width
        self.setMinimumWidth(self.minimum_width)
        self.icon_path = icon_path
        self.icon_path_close = icon_path_close
        self.parent = parent
        self._app_parent = app_parent
        self.menu_model: list[LeftMenuModel] = []

        self.left_menu_layout = QVBoxLayout(self)
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)

        # 全局
        self.bg = QFrame()
        self.left_menu_layout.addWidget(self.bg)
        self.bg.setStyleSheet(f"""
            background: {THEME.bg_300}; 
            border-radius: {THEME.border_radius};
        """)
        self._layout = QVBoxLayout(self.bg)
        self._layout.setContentsMargins(0, 0, 0, 0)

        # 上面
        self.top_frame = QFrame()
        self.top_layout = QVBoxLayout(self.top_frame)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(1)

        # 下面
        self.bottom_frame = QFrame()
        self.bottom_layout = QVBoxLayout(self.bottom_frame)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(1)

        self._layout.addWidget(self.top_frame, 0, Qt.AlignTop)  # type: ignore
        self._layout.addWidget(self.bottom_frame, 0, Qt.AlignBottom)  # type: ignore

        self.toggle_button = MangoMenuButton(
            app_parent,
            text=toggle_text,
            tooltip_text=toggle_tooltip,
            icon_path=icon_path
        )
        self.toggle_button.clicked.connect(lambda: self.toggle_animation(True))
        self.top_layout.addWidget(self.toggle_button)

        self.div_top = MangoDiv(THEME.bg_300)
        self.top_layout.addWidget(self.div_top)

        self.div_bottom = MangoDiv(THEME.bg_300)
        self.div_bottom.hide()
        self.bottom_layout.addWidget(self.div_bottom)

    def add_menus(self, menu_model: list[LeftMenuModel]):
        """
        添加菜单项
        
        根据菜单模型列表创建菜单按钮，支持主菜单和子菜单。
        
        参数:
            menu_model: 菜单模型列表
        """
        self.menu_model = menu_model
        for menu_obj in self.menu_model:
            layout = QVBoxLayout()
            menu_obj.but_obj = MangoMenuButton(
                self._app_parent,
                text=menu_obj.btn_text,
                btn_id=menu_obj.btn_id,
                tooltip_text=menu_obj.btn_tooltip,
                icon_path=menu_obj.btn_icon,
                is_active=menu_obj.is_active,
                url=menu_obj.url
            )
            # 捕获当前值
            menu_obj.but_obj.clicked.connect(lambda _, m=menu_obj: self.btn_clicked(_, m))
            menu_obj.but_obj.released.connect(lambda m=menu_obj: self.btn_released(m))
            layout.addWidget(menu_obj.but_obj)
            if menu_obj.submenus:
                frame_object = QFrame()
                frame_object.setStyleSheet("QFrame { border: none; }")
                frame_object.setContentsMargins(0, 0, 0, 0)
                frame_object.hide()
                v_layout = QVBoxLayout(frame_object)
                v_layout.setContentsMargins(0, 0, 0, 0)
                v_layout.setStretch(0, 7)
                for submenus in menu_obj.submenus:
                    menu_obj.frame_object = frame_object
                    frame_layout = QHBoxLayout()
                    submenus.but_obj = MangoMenuButton(
                        self._app_parent,
                        text=submenus.btn_text,
                        btn_id=submenus.btn_id,
                        tooltip_text=submenus.btn_tooltip,
                        icon_path=submenus.btn_icon,
                        is_active=submenus.is_active,
                    )
                    frame_layout.addWidget(submenus.but_obj)
                    v_layout.addLayout(frame_layout)
                    # 捕获当前值
                    submenus.but_obj.clicked.connect(lambda _, s=submenus: self.btn_clicked(_, s))
                    submenus.but_obj.released.connect(lambda s=submenus: self.btn_released(s))
                layout.addWidget(frame_object)
            if menu_obj.show_top:
                self.top_layout.addLayout(layout)
            else:
                self.div_bottom.show()
                self.bottom_layout.addLayout(layout)

    def btn_clicked(self, _, menu_obj):
        """
        菜单按钮点击事件处理
        
        参数:
            _: 事件对象（未使用）
            menu_obj: 菜单模型对象
        """
        self.clicked.emit(menu_obj)

    def btn_released(self, menu_obj):
        """
        菜单按钮释放事件处理
        
        参数:
            menu_obj: 菜单模型对象
        """
        self.released.emit(menu_obj)

    def toggle_animation(self, is_collect=True):
        """
        切换菜单展开/折叠动画
        
        参数:
            is_collect: 是否折叠，默认 True（折叠）
        """
        self.animation = QPropertyAnimation(self.parent, b"minimumWidth")
        self.animation.stop()
        current_width = self.width()
        if current_width == self.minimum_width:
            self.animation.setStartValue(current_width)
            self.animation.setEndValue(self.maximum_width)
            self.toggle_button.set_active_toggle(True)
            self.toggle_button.set_icon(self.icon_path_close)
        elif is_collect:
            self.animation.setStartValue(current_width)
            self.animation.setEndValue(self.minimum_width)
            self.toggle_button.set_active_toggle(False)
            self.toggle_button.set_icon(self.icon_path)
        else:
            # 确保在所有情况下都设置动画值
            self.animation.setStartValue(current_width)
            self.animation.setEndValue(current_width)  # 保持当前宽度
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)  # type: ignore
        self.animation.setDuration(self.duration_time)
        self.animation.start()

    def select_only_one(self, widget: str):
        """
        只选中指定的菜单按钮
        
        取消所有其他按钮的激活状态，只激活指定ID的按钮。
        
        参数:
            widget: 要激活的按钮ID
        """
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == widget:
                btn.set_active(True)
            else:
                btn.set_active(False)

    def select_only_one_tab(self, widget: str):
        """
        只选中指定的标签页按钮
        
        取消所有其他标签页按钮的激活状态，只激活指定ID的标签页按钮。
        
        参数:
            widget: 要激活的标签页按钮ID
        """
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == widget:
                btn.set_active_tab(True)
            else:
                btn.set_active_tab(False)

    def deselect_all(self):
        """
        取消所有菜单按钮的激活状态
        """
        for btn in self.findChildren(QPushButton):
            btn.set_active(False)

    def deselect_all_tab(self):
        """
        取消所有标签页按钮的激活状态
        """
        for btn in self.findChildren(QPushButton):
            btn.set_active_tab(False)
