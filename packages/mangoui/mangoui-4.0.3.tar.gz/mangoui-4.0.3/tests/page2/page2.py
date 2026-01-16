# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 使用主窗口类型2 (MangoMain2Window) 的简单测试入口，包含默认菜单
# @Time   : 2025-01-14
# @Author : 毛鹏

import os
import sys

# 保证可以找到项目根目录下的 mangoui 包（与 tests/pages/main.py 保持一致写法）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from PySide6.QtWidgets import QApplication

from mangoui.models.models import AppConfig, MenusModel, LeftMenuModel
from mangoui.widgets.window import MangoMain2Window
from mangoui.settings.settings import STYLE as DEFAULT_STYLE
from tests.page2.home import HomePage
from tests.page2.window import WindowPage
from tests.page2.form import FormPage
from tests.page2.chart import ChartPage
from tests.page2.about import AboutPage
from tests.page2.request import RequestPage


def build_default_style() -> AppConfig:
    """
    构建一个简单的默认应用样式配置
    """
    # 直接复用全局 STYLE，避免缺少 AppConfig 必填字段
    return DEFAULT_STYLE


def build_default_menus() -> MenusModel:
    """
    构建一些默认菜单项，用于演示菜单样式2
    """
    # 6 个带图标的菜单：首页 / 窗口 / 表单 / 图表 / 请求 / 关于
    left_menus: list[LeftMenuModel] = [
        LeftMenuModel(
            btn_id="home",
            btn_text="首页",
            btn_icon=":/icons/home.svg",
            btn_tooltip="首页",
            is_active=True,
            show_top=True,
            submenus=[],
        ),
        LeftMenuModel(
            btn_id="window",
            btn_text="窗口组件",
            btn_icon=":/icons/desktop.svg",
            btn_tooltip="窗口组件示例",
            is_active=False,
            show_top=True,
            submenus=[],
        ),
        LeftMenuModel(
            btn_id="form",
            btn_text="表单",
            btn_icon=":/icons/menu.svg",
            btn_tooltip="表单示例",
            is_active=False,
            show_top=True,
            submenus=[],
        ),
        LeftMenuModel(
            btn_id="chart",
            btn_text="图表",
            btn_icon=":/icons/app_icon.svg",
            btn_tooltip="图表示例",
            is_active=False,
            show_top=True,
            submenus=[],
        ),
        LeftMenuModel(
            btn_id="request",
            btn_text="模拟请求",
            btn_icon=":/icons/menu.svg",
            btn_tooltip="模拟请求（标准库）",
            is_active=False,
            show_top=True,
            submenus=[],
        ),
        LeftMenuModel(
            btn_id="about",
            btn_text="关于",
            btn_icon=":/icons/info.svg",
            btn_tooltip="关于 MangoUI",
            is_active=False,
            show_top=True,
            submenus=[],
        ),
    ]

    # 顶部标题栏菜单保持空，main_2 不使用
    title_bar_menus: list[LeftMenuModel] = []

    menus = MenusModel(
        left_menus=left_menus,
        title_bar_menus=title_bar_menus,
    )
    return menus


def build_page_dict():
    """
    页面字典映射
    """
    return {
        "home": HomePage,
        "window": WindowPage,
        "form": FormPage,
        "chart": ChartPage,
        "request": RequestPage,
        "about": AboutPage,
    }


def main():
    import sys as _sys

    app = QApplication(_sys.argv)
    style = build_default_style()
    menus = build_default_menus()
    page_dict = build_page_dict()

    # main_2 采用自定义顶部+左侧一体化菜单，不再需要额外 customize_titlebar 参数
    window = MangoMain2Window(style, menus, page_dict, width_coefficient=0.3, height_coefficient=0.6)
    window.show()

    _sys.exit(app.exec())


if __name__ == "__main__":
    main()

