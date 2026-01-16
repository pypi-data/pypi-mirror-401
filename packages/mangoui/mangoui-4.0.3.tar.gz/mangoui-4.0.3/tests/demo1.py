from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTextEdit, QLabel, QSizePolicy, QApplication, QMainWindow)


class ResponsiveLayoutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # 标题栏 - 固定高度
        title_label = QLabel("自适应界面")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        main_layout.addWidget(title_label)

        # 内容区域 - 可扩展
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)

        # 左侧面板 - 固定宽度比例
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        for i in range(5):
            btn = QPushButton(f"按钮 {i + 1}")
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            left_layout.addWidget(btn)

        # 右侧面板 - 可扩展
        right_panel = QTextEdit()
        right_panel.setPlaceholderText("编辑区域")

        # 设置面板大小策略
        left_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        right_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        content_layout.addWidget(left_panel, 1)  # 权重1
        content_layout.addWidget(right_panel, 3)  # 权重3

        main_layout.addWidget(content_widget)

        # 状态栏 - 固定高度
        status_label = QLabel("就绪")
        status_label.setStyleSheet("padding: 5px; background-color: #f0f0f0;")
        status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(status_label)

        self.setWindowTitle('响应式布局')
        self.resize_to_percentage(0.7, 0.7)

    def resize_to_percentage(self, width_percent=0.7, height_percent=0.7):
        """按屏幕百分比调整窗口大小"""
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * width_percent)
        height = int(screen.height() * height_percent)
        self.resize(width, height)
        self.center_on_screen()

    def center_on_screen(self):
        """窗口居中"""
        screen = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())