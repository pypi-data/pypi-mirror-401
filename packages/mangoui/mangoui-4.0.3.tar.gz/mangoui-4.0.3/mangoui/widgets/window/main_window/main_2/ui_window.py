# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 主窗口 UI 类型2 - 使用菜单样式2 的主窗口
# @Time   : 2025-01-14
# @Author : 毛鹏

import webbrowser

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.models.models import MenusModel, AppConfig, LeftMenuModel
from mangoui.settings.settings import THEME
from mangoui.widgets.miscellaneous.mango_credits import MangoCredits
from mangoui.widgets.miscellaneous.mango_grips import MangoGrips
from mangoui.widgets.title_bar.mango_title_button_main2 import MangoTitleButtonMain2
from mangoui.widgets.window.main_window.main_2.pages_window import PagesWindow
from mangoui.widgets.window.main_window.main_2.menu_style2 import MangoMenuStyle2
from mangoui.widgets.window.mango_frame import MangoFrame

_is_maximized = False
_old_size = QSize()
class UIWindow2(QMainWindow):
    """
    主窗口 UI 类型2

    基于现有 UIWindow 逻辑，左侧菜单替换为 `MangoMenuStyle2`，
    实现类似图片中的现代化菜单效果。
    """

    clicked = Signal(object)

    def __init__(self, style: AppConfig, menus: MenusModel, page_dict, l=None, **kwargs):
        super().__init__()
        self.style = style
        self.menus = menus
        self.loop = l
        self.page_dict = page_dict
        self.kwargs = kwargs
        self.page = None
        self.setWindowTitle(self.style.app_name)
        # 拖动用坐标
        self.drag_pos = QPoint()

        # 根据当前屏幕分辨率和可用区域，自适应设置窗口大小
        screen = QGuiApplication.primaryScreen()
        geometry = screen.availableGeometry() if screen is not None else QRect(0, 0, 1600, 900)

        # 默认宽高系数，可通过 kwargs 覆盖
        width_coefficient = kwargs.get('width_coefficient', 0.6)
        height_coefficient = kwargs.get('height_coefficient', 0.7)

        base_width = int(geometry.width() * width_coefficient)
        base_height = int(geometry.height() * height_coefficient)

        # 设定一个合理的最小/最大像素范围，兼容低分辨率和 2K/4K 屏幕
        min_width, min_height = 960, 540
        max_width, max_height = int(geometry.width() * 0.9), int(geometry.height() * 0.9)

        width = max(min_width, min(base_width, max_width))
        height = max(min_height, min(base_height, max_height))

        self.resize(width, height)
        # 最小尺寸设置得相对宽松一些，方便在小屏幕上缩放
        self.setMinimumSize(int(width * 0.6), int(height * 0.6))

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(f'''
            font: {THEME.font.text_size}pt "{THEME.font.family}";
            color: {THEME.text_100};
        ''')
        self.central_widget_layout = QVBoxLayout(self.central_widget)
        # main_2 使用自定义头部卡片，保留一定外边距
        self.central_widget_layout.setContentsMargins(10, 10, 10, 10)
        self.setCentralWidget(self.central_widget)

        # 使用无边框窗口 + 背景透明，让自定义头部与左侧菜单整体显示
        self.setWindowFlag(Qt.FramelessWindowHint)  # type: ignore
        self.setAttribute(Qt.WA_TranslucentBackground)  # type: ignore

        # 外层应用卡片
        self.window = MangoFrame(self)
        self.window.set_stylesheet()
        self.central_widget_layout.addWidget(self.window)

        # 内部容器：先是顶部横向栏，再是左侧菜单 + 右侧内容
        self.window_container = QFrame()
        self.window_container_layout = QVBoxLayout(self.window_container)
        self.window_container_layout.setContentsMargins(0, 0, 0, 0)
        self.window_container_layout.setSpacing(0)
        self.window.layout.addWidget(self.window_container)

        # 顶部横向浅色栏（Logo + 顶部菜单 + 窗口按钮）
        self.header_frame = QFrame()
        self.header_frame.setObjectName("main2HeaderFrame")
        # 顶部 title 区比之前略矮一点，让整体更紧凑
        self.header_frame.setFixedHeight(36)
        self.header_frame.setStyleSheet(f"""
            QFrame#main2HeaderFrame {{
                background-color: {THEME.bg_300};
                border-bottom: 1px solid {THEME.bg_300};
            }}
        """)
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(16, 0, 16, 0)
        self.header_layout.setSpacing(16)

        # 左侧 Logo / 标题
        self.header_title_label = QLabel(self.style.app_name)
        self.header_title_label.setStyleSheet(f"""
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.title_size + 2}px;
            font-weight: 600;
        """)
        self.header_layout.addWidget(self.header_title_label)

        # 中间留白
        self.header_layout.addStretch()

        # 中间留白，直接把窗口控制按钮推到最右侧（不再需要顶部“概览/组件/文档”菜单）
        self.header_layout.addStretch()

        # 窗口控制按钮：最小化 / 最大化 / 关闭
        self.minimize_button = MangoTitleButtonMain2(
            self,
            self.central_widget,
            tooltip_text="",
            icon_path=":/icons/icon_minimize.svg",
        )
        self.maximize_restore_button = MangoTitleButtonMain2(
            self,
            self.central_widget,
            tooltip_text="",
            icon_path=":/icons/icon_maximize.svg",
        )
        self.close_button = MangoTitleButtonMain2(
            self,
            self.central_widget,
            tooltip_text="",
            icon_path=":/icons/icon_close.svg",
        )

        self.minimize_button.released.connect(lambda: self.showMinimized())
        self.maximize_restore_button.released.connect(self.maximize_restore)
        self.close_button.released.connect(lambda: self.close())

        self.header_layout.addWidget(self.minimize_button)
        self.header_layout.addWidget(self.maximize_restore_button)
        self.header_layout.addWidget(self.close_button)

        # 允许通过头部区域拖动窗口
        def move_window(event):
            if event.buttons() == Qt.LeftButton:  # type: ignore
                self.move(self.pos() + event.globalPos() - self.drag_pos)
                self.drag_pos = event.globalPos()
                event.accept()

        def header_mouse_press(event):
            if event.button() == Qt.LeftButton:  # type: ignore
                self.drag_pos = event.globalPos()

        self.header_frame.mouseMoveEvent = move_window
        self.header_frame.mousePressEvent = header_mouse_press

        self.window_container_layout.addWidget(self.header_frame)

        # 主体区域：左侧菜单 + 右侧内容
        self.body_frame = QFrame()
        self.body_layout = QHBoxLayout(self.body_frame)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(0)
        self.window_container_layout.addWidget(self.body_frame)

        # 先创建右侧内容容器，再创建左侧菜单，保证结构清晰
        self.right_app_frame = QFrame()
        self.right_app_layout = QVBoxLayout(self.right_app_frame)
        # 左边和上边为0，让内容区域紧贴左侧菜单和顶部titlebar的交汇处，实现左上角圆角效果
        self.right_app_layout.setContentsMargins(0, 0, 16, 16)
        self.right_app_layout.setSpacing(8)
        self.body_layout.addWidget(self.right_app_frame, 1)

        # 左侧菜单
        self.menus_ui()

        # main_2 使用自定义 header_frame，不再创建单独的窗口级标题栏
        self.content_ui()
        self.bottom_ui()

    def menus_ui(self):
        """左侧菜单区域 - 使用 MangoMenuStyle2"""
        self.left_menu_frame = QFrame()
        # main_2 左侧菜单：在此前基础上略微收窄一点，让右侧内容区域更宽
        left_menu_width = int(self.style.lef_menu_size.minimum * 1.3)
        self.left_menu_frame.setMaximumSize(
            left_menu_width + (self.style.left_menu_content_margins * 2), 17280)
        self.left_menu_frame.setMinimumSize(
            left_menu_width + (self.style.left_menu_content_margins * 2), 0)
        # 与顶部标题栏视觉上一体：使用同样的浅色背景，由这一层统一作为“左侧整块区域”
        self.left_menu_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {THEME.bg_300};
                border: none;
            }}
        """)
        self.left_menu_layout = QHBoxLayout(self.left_menu_frame)
        # 取消多余边距，让菜单与标题栏的卡片边缘对齐
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)

        self.left_menu = MangoMenuStyle2(
            parent=self.left_menu_frame,
            app_parent=self.central_widget,
            width=left_menu_width,
        )
        self.left_menu.add_menus(self.menus.left_menus)
        self.left_menu.clicked.connect(self.btn_clicked)
        self.left_menu.released.connect(self.btn_released)
        self.left_menu_layout.addWidget(self.left_menu)
        # 左侧菜单放在主体区域左侧，与顶部横向栏视觉连贯
        self.body_layout.insertWidget(0, self.left_menu_frame)

    def title_bar_ui(self):
        # main_2 使用自定义 header_frame，不再使用 MangoTitleBar
        return

    def content_ui(self):
        self.content_area_frame = QFrame()
        self.content_area_layout = QHBoxLayout(self.content_area_frame)
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area_layout.setSpacing(0)

        self.content_area_left_frame = QFrame()
        self.content_area_left_frame.setObjectName("contentAreaLeftFrame")
        # 设置左上角圆角，让内容区域在菜单和titlebar的内角处形成圆角效果
        self.content_area_left_frame.setStyleSheet(f"""
            QFrame#contentAreaLeftFrame {{
                background-color: {THEME.bg_100};
                border: none;
                border-top-left-radius: 12px;
            }}
        """)

        self.load_pages = PagesWindow(self, self.content_area_left_frame, self.page_dict)

        self.load_pages.set_page(self.kwargs.get('page') if self.kwargs.get('page') else 'home')
        self.content_area_layout.addWidget(self.content_area_left_frame)
        self.right_app_layout.addWidget(self.content_area_frame)
        self.right_app_layout.setStretch(1, 1)  # 让内容区域占据剩余空间

    def bottom_ui(self):
        """
        底部区域

        main_2 设计中，默认不再展示底部 title_bar / 版权栏，
        让视觉焦点集中在顶部 titlebar + 左侧菜单的一体区域。

        如果后续需要显示底部版权信息，可以在创建窗口时传入
        `show_bottom_bar=True`，再恢复添加。
        """
        if not self.kwargs.get('show_bottom_bar', False):
            # 不添加任何底部条，直接返回
            return

        self.credits_frame = QFrame()
        self.credits_frame.setMinimumHeight(28)
        self.credits_frame.setMaximumHeight(28)
        self.credits_layout = QVBoxLayout(self.credits_frame)
        self.credits_layout.setContentsMargins(0, 0, 0, 0)
        self.credits = MangoCredits(self.style.copyright, self.style.version)
        self.credits_layout.addWidget(self.credits)
        self.right_app_layout.addWidget(self.credits_frame)

    def btn_released(self):
        _ = self.__setup_btn()

    def title_ber_but_clicked(self):
        """
        标题栏按钮点击（仅在使用自定义标题栏时才会触发）
        """
        btn = self.__setup_btn()
        if not btn:
            return
        if getattr(btn, "url", None):
            webbrowser.open(btn.url)
            return
        btn_name = btn.objectName()
        self.clicked.emit(btn_name)

    def btn_clicked(self, menu_obj: LeftMenuModel):
        if menu_obj.url:
            webbrowser.open(menu_obj.url)
            return

        # 折叠/展开子菜单（如果有）
        for i in self.menus.left_menus:
            if i.btn_id != menu_obj.btn_id and i.frame_object and menu_obj.btn_id not in [e.btn_id for e in i.submenus]:
                i.frame_object.hide()

        # 页面切换
        self.left_menu.select_only_one(menu_obj.btn_id)
        self.load_pages.set_page(menu_obj.btn_id)

    def get_title_bar_btn(self, object_name):
        # main_2 使用自定义 header_frame，而非 MangoTitleBar
        return None

    def __setup_btn(self):
        # 仅从左侧菜单获取 sender
        if self.left_menu.sender() is not None:
            return self.left_menu.sender()
        return None

    def resize_grips(self):
        """
        调整无边框窗口四周拖拽区域大小

        main_2 默认不使用自定义标题栏和拖拽 grip，
        只有在创建了这些 grip 属性时才需要调整。
        """
        # 如果没有创建 grip，则直接返回
        if not hasattr(self, "left_grip"):
            return
        self.left_grip.setGeometry(5, 10, 10, self.height())
        self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
        self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
        self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
        self.top_left_grip.setGeometry(self.width() - 20, 5, 15, 15)
        self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
        self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
        self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)

    def set_page(self, page: str, data: dict | None = None):
        self.load_pages.set_page(page, data)

    def maximize_restore(self, e=None):
        """
        最大化并恢复窗口

        切换窗口的最大化和正常状态，并更新 UI 样式。
        """
        # 使用模块级变量记录状态
        global _is_maximized
        global _old_size

        def change_ui():
            if _is_maximized:
                # 最大化：去掉外层圆角和边距
                self.central_widget_layout.setContentsMargins(0, 0, 0, 0)
                self.window.set_stylesheet(border_radius=0, border_size=0)
                self.maximize_restore_button.set_icon(":/icons/icon_restore.svg")
            else:
                # 恢复：恢复卡片效果
                self.central_widget_layout.setContentsMargins(10, 10, 10, 10)
                self.window.set_stylesheet()
                self.maximize_restore_button.set_icon(":/icons/icon_maximize.svg")

        if self.isMaximized():
            _is_maximized = False
            self.showNormal()
            change_ui()
        else:
            _is_maximized = True
            _old_size = QSize(self.width(), self.height())
            self.showMaximized()
            change_ui()

