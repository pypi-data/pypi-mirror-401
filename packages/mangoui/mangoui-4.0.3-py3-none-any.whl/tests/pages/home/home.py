# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 首页 - 展示MangoUI组件库的介绍和统计信息
# @Time   : 2024-11-02 21:24
# @Author : 毛鹏

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from mangoui.widgets.container import MangoCard
from mangoui.widgets.display import MangoLabel
from mangoui.widgets.layout import MangoVBoxLayout, MangoHBoxLayout, MangoGridLayout
from mangoui.widgets.window import MangoScrollArea
from mangoui.settings.settings import THEME


class HomePage(QWidget):
    """
    首页组件
    
    展示MangoUI组件库的项目介绍、组件统计、核心特性等信息。
    使用全局主题配置确保样式统一，优化布局以适应单页展示。
    """
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = MangoVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # 创建滚动区域以容纳所有组件
        self.scroll_area = MangoScrollArea()
        self.scroll_layout = self.scroll_area.layout
        self.scroll_layout.setAlignment(Qt.AlignTop)  # type: ignore
        # 设置滚动布局的边距，紧凑但美观
        self.scroll_layout.setContentsMargins(40, 30, 40, 30)
        self.scroll_layout.setSpacing(25)
        
        # 1. 标题区域 - 使用主题渐变色
        self._create_title_section()
        
        # 2. 项目介绍区域
        self._create_intro_section()
        
        # 3. 组件统计区域 - 使用网格布局
        self._create_stats_section()
        
        # 4. 核心特性区域
        self._create_features_section()
        
        # 5. 快速开始区域
        self._create_quick_start_section()
        
        # 设置滚动区域
        self.layout.addWidget(self.scroll_area)
    
    def _create_title_section(self):
        """创建标题区域"""
        title_container = QWidget()
        title_container.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {THEME.primary_100}, stop:1 {THEME.primary_300});
                border-radius: {THEME.border_radius};
                padding: 30px 20px;
            }}
        """)
        title_layout = MangoVBoxLayout(title_container)
        title_layout.setSpacing(12)
        
        # 主标题
        title = MangoLabel("芒果PySide6组件库")
        title.setStyleSheet(f"""
            font-size: 36px; 
            font-weight: bold; 
            color: {THEME.text_100};
            background: transparent;
            border: none;
        """)
        title.setAlignment(Qt.AlignCenter)  # type: ignore
        title_layout.addWidget(title)
        
        # 副标题
        subtitle = MangoLabel("MangoUI - Modern PySide6 Component Library")
        subtitle.setStyleSheet(f"""
            font-size: 16px; 
            color: {THEME.text_200};
            background: transparent;
            border: none;
            font-weight: normal;
        """)
        subtitle.setAlignment(Qt.AlignCenter)  # type: ignore
        title_layout.addWidget(subtitle)
        
        self.scroll_layout.addWidget(title_container)
    
    def _create_intro_section(self):
        """创建项目介绍区域"""
        intro_card_layout = MangoVBoxLayout()
        intro_card_layout.setSpacing(15)
        intro_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # 介绍标题
        intro_title = MangoLabel("关于 MangoUI")
        intro_title.setStyleSheet(f"""
            font-size: 20px; 
            font-weight: bold; 
            color: {THEME.text_100};
            background: transparent;
            border: none;
            margin-bottom: 10px;
        """)
        intro_card_layout.addWidget(intro_title)
        
        # 介绍内容
        intro_text = MangoLabel(
            "MangoUI 是一个基于 PySide6 的现代化 UI 组件库，提供了丰富的组件和布局方案。"
            "通过统一的主题配置和样式系统，帮助开发者快速构建美观、一致的桌面应用程序。"
            "\n\n"
            "组件库涵盖了输入组件、显示组件、容器组件、菜单组件、图表组件等多个类别，"
            "每个组件都经过精心设计，确保样式统一、交互流畅。"
        )
        intro_text.setStyleSheet(f"""
            font-size: 14px; 
            color: {THEME.text_200};
            background: transparent;
            border: none;
            line-height: 1.8;
        """)
        intro_text.setWordWrap(True)
        intro_card_layout.addWidget(intro_text)
        
        # 创建介绍卡片
        intro_card = MangoCard(intro_card_layout)
        intro_card.setStyleSheet(f"""
            QFrame#cardFrame {{
                background-color: {THEME.bg_200};
                border: {THEME.border};
                border-radius: {THEME.border_radius};
            }}
        """)
        self.scroll_layout.addWidget(intro_card)
    
    def _create_stats_section(self):
        """创建组件统计区域"""
        # 统计标题
        stats_title = MangoLabel("组件统计")
        stats_title.setStyleSheet(f"""
            font-size: 22px; 
            font-weight: bold; 
            color: {THEME.text_100};
            background: transparent;
            border: none;
            margin-top: 10px;
        """)
        self.scroll_layout.addWidget(stats_title)
        
        # 使用网格布局展示统计卡片
        stats_grid = MangoGridLayout()
        stats_grid.setSpacing(15)
        stats_grid.setContentsMargins(0, 0, 0, 0)
        
        # 定义卡片配置 - 使用主题颜色
        card_configs = [
            {
                "title": "输入组件",
                "count": "17+",
                "desc": "按钮、输入框、选择器等",
                "color": THEME.primary_100,
                "bg": THEME.primary_300
            },
            {
                "title": "显示组件",
                "count": "18+",
                "desc": "标签、表格、列表、进度条等",
                "color": THEME.accent_100,
                "bg": THEME.bg_200
            },
            {
                "title": "容器组件",
                "count": "5+",
                "desc": "卡片、分组框、堆叠窗口等",
                "color": THEME.primary_200,
                "bg": THEME.primary_300
            },
            {
                "title": "菜单组件",
                "count": "3+",
                "desc": "菜单栏、工具栏、标签页等",
                "color": THEME.accent_200,
                "bg": THEME.bg_200
            },
        ]
        
        for idx, config in enumerate(card_configs):
            card = self._create_stat_card(config)
            # 2列布局
            row = idx // 2
            col = idx % 2
            stats_grid.addWidget(card, row, col)
        
        stats_widget = QWidget()
        stats_widget.setLayout(stats_grid)
        self.scroll_layout.addWidget(stats_widget)
    
    def _create_stat_card(self, config: dict) -> MangoCard:
        """创建单个统计卡片"""
        card_layout = MangoVBoxLayout()
        card_layout.setSpacing(8)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setAlignment(Qt.AlignCenter)  # type: ignore
        
        # 数量标签
        count_label = MangoLabel(config["count"])
        count_label.setStyleSheet(f"""
            font-size: 32px; 
            font-weight: bold; 
            color: {config["color"]};
            background: transparent;
            border: none;
        """)
        count_label.setAlignment(Qt.AlignCenter)  # type: ignore
        card_layout.addWidget(count_label)
        
        # 标题标签
        title_label = MangoLabel(config["title"])
        title_label.setStyleSheet(f"""
            font-size: 16px; 
            font-weight: bold;
            color: {THEME.text_100};
            background: transparent;
            border: none;
        """)
        title_label.setAlignment(Qt.AlignCenter)  # type: ignore
        card_layout.addWidget(title_label)
        
        # 描述标签
        desc_label = MangoLabel(config["desc"])
        desc_label.setStyleSheet(f"""
            font-size: 12px; 
            color: {THEME.text_200};
            background: transparent;
            border: none;
        """)
        desc_label.setAlignment(Qt.AlignCenter)  # type: ignore
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        # 创建卡片
        card = MangoCard(card_layout, title=None)
        card.setStyleSheet(f"""
            QFrame#cardFrame {{
                background-color: {config["bg"]};
                border: 2px solid {config["color"]}40;
                border-radius: {THEME.border_radius};
            }}
            QFrame#cardFrame:hover {{
                border: 2px solid {config["color"]};
                background-color: {config["bg"]}dd;
            }}
        """)
        card.setMinimumHeight(140)
        card.setMinimumWidth(200)
        
        return card
    
    def _create_features_section(self):
        """创建核心特性区域"""
        # 特性标题
        features_title = MangoLabel("核心特性")
        features_title.setStyleSheet(f"""
            font-size: 22px; 
            font-weight: bold; 
            color: {THEME.text_100};
            background: transparent;
            border: none;
            margin-top: 10px;
        """)
        self.scroll_layout.addWidget(features_title)
        
        # 创建特性内容布局
        features_layout = MangoVBoxLayout()
        features_layout.setSpacing(12)
        features_layout.setContentsMargins(20, 20, 20, 20)
        
        features = [
            ("🎨", "现代化UI设计", "统一的主题配置系统，支持全局样式定制，确保界面美观一致"),
            ("📦", "丰富的组件库", "涵盖输入、显示、容器、菜单、图表等多个类别，满足各种开发需求"),
            ("📱", "响应式布局", "灵活的布局系统，适配不同屏幕尺寸和分辨率"),
            ("🔧", "易于扩展", "清晰的组件结构，支持自定义样式和行为，方便二次开发"),
            ("📚", "完善文档", "详细的组件文档和使用示例，快速上手开发")
        ]
        
        for icon, title, desc in features:
            feature_item = self._create_feature_item(icon, title, desc)
            features_layout.addWidget(feature_item)
        
        # 创建特性卡片
        features_card = MangoCard(features_layout)
        features_card.setStyleSheet(f"""
            QFrame#cardFrame {{
                background-color: {THEME.bg_100};
                border: {THEME.border};
                border-radius: {THEME.border_radius};
            }}
        """)
        self.scroll_layout.addWidget(features_card)
    
    def _create_feature_item(self, icon: str, title: str, desc: str) -> QWidget:
        """创建单个特性项"""
        feature_container = QWidget()
        feature_container.setStyleSheet(f"""
            QWidget {{
                background-color: {THEME.bg_200};
                border-left: 4px solid {THEME.primary_100};
                border-radius: 4px;
                padding: 0px;
            }}
        """)
        feature_layout = MangoHBoxLayout(feature_container)
        feature_layout.setContentsMargins(15, 12, 15, 12)
        feature_layout.setSpacing(12)
        
        # 图标标签
        icon_label = MangoLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            background: transparent;
            border: none;
        """)
        icon_label.setFixedWidth(40)
        feature_layout.addWidget(icon_label)
        
        # 内容布局
        content_layout = MangoVBoxLayout()
        content_layout.setSpacing(4)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题
        title_label = MangoLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 15px; 
            font-weight: bold;
            color: {THEME.text_100};
            background: transparent;
            border: none;
        """)
        content_layout.addWidget(title_label)
        
        # 描述
        desc_label = MangoLabel(desc)
        desc_label.setStyleSheet(f"""
            font-size: 13px; 
            color: {THEME.text_200};
            background: transparent;
            border: none;
        """)
        desc_label.setWordWrap(True)
        content_layout.addWidget(desc_label)
        
        feature_layout.addLayout(content_layout)
        feature_layout.addStretch()
        
        return feature_container
    
    def _create_quick_start_section(self):
        """创建快速开始区域"""
        quick_start_layout = MangoVBoxLayout()
        quick_start_layout.setSpacing(15)
        quick_start_layout.setContentsMargins(20, 20, 20, 20)
        
        # 快速开始标题
        quick_start_title = MangoLabel("快速开始")
        quick_start_title.setStyleSheet(f"""
            font-size: 20px; 
            font-weight: bold; 
            color: {THEME.text_100};
            background: transparent;
            border: none;
        """)
        quick_start_layout.addWidget(quick_start_title)
        
        # 使用说明
        usage_text = MangoLabel(
            "1. 通过左侧导航菜单浏览不同类型的组件示例\n"
            "2. 每个组件页面都提供了详细的使用示例和代码\n"
            "3. 所有组件都使用统一的主题配置，确保样式一致\n"
            "4. 可以根据需要自定义主题颜色和样式"
        )
        usage_text.setStyleSheet(f"""
            font-size: 14px; 
            color: {THEME.text_200};
            background: transparent;
            border: none;
            line-height: 2.0;
        """)
        usage_text.setWordWrap(True)
        quick_start_layout.addWidget(usage_text)
        
        # 创建快速开始卡片
        quick_start_card = MangoCard(quick_start_layout)
        quick_start_card.setStyleSheet(f"""
            QFrame#cardFrame {{
                background-color: {THEME.primary_300};
                border: {THEME.border};
                border-radius: {THEME.border_radius};
            }}
        """)
        self.scroll_layout.addWidget(quick_start_card)
        
        # 添加底部间距
        self.scroll_layout.addStretch()
