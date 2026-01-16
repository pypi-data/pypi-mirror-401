# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 菜单样式2组件 - 基于图片的现代化侧边菜单样式
# @Time   : 2025-01-14
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.models.models import LeftMenuModel
from mangoui.settings.settings import THEME
from .menu_button_style2 import MangoMenuButtonStyle2


class MangoMenuStyle2(QWidget):
    """
    菜单样式2组件
    
    基于图片样式的现代化侧边菜单，支持：
    - 激活项：浅灰色背景 + 左侧蓝色垂直条 + 蓝色图标
    - 非激活项：透明背景 + 灰色图标
    - 圆角设计
    - 图标+文字组合
    
    信号:
        clicked: 当菜单项被点击时触发，传递菜单模型
        released: 当菜单项被释放时触发，传递菜单模型
    
    参数:
        parent: 父组件
        app_parent: 应用程序父组件
        width: 菜单宽度，默认 200
        spacing: 菜单项间距，默认 4
    
    示例:
        >>> menu = MangoMenuStyle2(parent, app_parent)
        >>> menu.add_menus([LeftMenuModel(...)])
    """
    clicked = Signal(LeftMenuModel)
    released = Signal(LeftMenuModel)

    def __init__(
            self,
            parent=None,
            app_parent=None,
            width=200,
            spacing=4,
    ):
        super().__init__()
        self.parent = parent
        self._app_parent = app_parent
        self.menu_model: list[LeftMenuModel] = []
        self.width = width
        self.spacing = spacing
        
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

        # 让自身背景透明，由外层容器（left_menu_frame + header_frame）统一控制区域背景
        self.setStyleSheet("""
            QWidget{
                background-color: transparent;
                border-radius: 0px;
            }
        """)

        # 主布局（左右边距设为0，让按钮在菜单列内真正居中）
        self.main_layout = QVBoxLayout(self)
        # 只保留上下边距，左右边距设为0，确保按钮在菜单列宽度内居中
        self.main_layout.setContentsMargins(0, 8, 0, 8)
        self.main_layout.setSpacing(self.spacing)

        # 顶部菜单区域（可滚动：菜单多时不被挤出窗口）
        self.top_scroll = QScrollArea()
        self.top_scroll.setFrameShape(QFrame.NoFrame)  # type: ignore
        self.top_scroll.setWidgetResizable(True)
        self.top_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # type: ignore
        self.top_scroll.setStyleSheet("QScrollArea { background: transparent; }")

        self.top_frame = QFrame()
        self.top_frame.setStyleSheet("QFrame { background: transparent; }")
        # 关键：让 top_frame 横向撑满 scroll viewport，否则按钮"在 frame 里居中"但整体看起来不居中
        self.top_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        # 设置最小宽度为菜单宽度，确保 frame 撑满整个菜单列
        self.top_frame.setMinimumWidth(width)
        self.top_layout = QVBoxLayout(self.top_frame)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(self.spacing)
        self.top_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)  # type: ignore
        self.top_scroll.setWidget(self.top_frame)

        # 底部菜单区域（用于用户头像等）
        self.bottom_frame = QFrame()
        # 底部区域也保持横向撑满，保证底部按钮同样左右居中
        self.bottom_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        # 设置最小宽度为菜单宽度，确保 frame 撑满整个菜单列
        self.bottom_frame.setMinimumWidth(width)
        self.bottom_layout = QVBoxLayout(self.bottom_frame)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(self.spacing)
        self.bottom_layout.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)  # type: ignore

        self.main_layout.addWidget(self.top_scroll, 1)  # 顶部菜单占据可用空间，可滚动
        self.main_layout.addWidget(self.bottom_frame, 0, Qt.AlignBottom)  # type: ignore

    def add_menus(self, menu_model: list[LeftMenuModel]):
        """
        添加菜单项
        
        根据菜单模型列表创建菜单按钮，支持主菜单和子菜单。
        
        参数:
            menu_model: 菜单模型列表
        """
        self.menu_model = menu_model

        for menu_obj in menu_model:
            if not menu_obj.show_top:
                continue
            
            # 创建菜单按钮（正方形按钮：图标 + 底部文字）
            btn = MangoMenuButtonStyle2(
                app_parent=self._app_parent,
                text=menu_obj.btn_text,
                tooltip_text="",  # main_2 设计中不需要悬停提示
                url=menu_obj.url,
                btn_id=menu_obj.btn_id,
                icon_path=menu_obj.btn_icon,
                is_active=menu_obj.is_active,
                height=60,  # 稍微小一点，避免菜单多时挤出可视区域
            )
            
            # 连接信号（自定义 QWidget 按钮的 clicked / released 不带 checked 参数）
            btn.clicked.connect(lambda m=menu_obj: self._btn_clicked(m))
            btn.released.connect(lambda m=menu_obj: self._btn_released(m))
            
            # 添加到顶部或底部，水平方向居中摆放正方形按钮
            if hasattr(menu_obj, 'is_bottom') and menu_obj.is_bottom:
                self.bottom_layout.addWidget(btn, 0, Qt.AlignHCenter)
            else:
                self.top_layout.addWidget(btn, 0, Qt.AlignHCenter)
            
            # 设置初始激活状态
            if menu_obj.is_active:
                self.select_only_one(menu_obj.btn_id)

    def _btn_clicked(self, menu_obj: LeftMenuModel):
        """菜单按钮点击事件处理"""
        self.clicked.emit(menu_obj)

    def _btn_released(self, menu_obj: LeftMenuModel):
        """菜单按钮释放事件处理"""
        self.released.emit(menu_obj)

    def select_only_one(self, widget: str):
        """
        只选中指定的菜单按钮
        
        取消所有其他按钮的激活状态，只激活指定ID的按钮。
        
        参数:
            widget: 要激活的按钮ID
        """
        for btn in self.findChildren(MangoMenuButtonStyle2):
            if btn.objectName() == widget:
                btn.set_active(True)
            else:
                btn.set_active(False)

    def deselect_all(self):
        """取消所有菜单按钮的激活状态"""
        for btn in self.findChildren(MangoMenuButtonStyle2):
            btn.set_active(False)
