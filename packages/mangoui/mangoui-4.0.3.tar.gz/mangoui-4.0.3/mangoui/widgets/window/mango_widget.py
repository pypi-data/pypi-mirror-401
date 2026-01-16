# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 基础窗口组件 - 提供统一的窗口组件基类和异步数据加载功能
# @Time   : 2025-05-25 23:31
# @Author : 毛鹏
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget

from mangoui.widgets.layout import MangoVBoxLayout


class DataLoadWorker(QThread):
    """
    数据加载工作线程
    
    用于在后台线程中加载页面数据，避免阻塞主界面。
    
    信号:
        finished: 当数据加载完成时触发
    """
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        """
        运行工作线程
        
        在后台线程中调用父组件的 load_page_data 方法加载数据。
        """
        try:
            self.parent.load_page_data()  # type: ignore
        finally:
            self.finished.emit()


class MangoWidget(QWidget):
    """
    基础窗口组件
    
    提供统一的窗口组件基类，支持异步数据加载功能。
    继承自 QWidget，使用 MangoVBoxLayout 作为默认布局。
    
    参数:
        parent: 父组件
        *args, **kwargs: 额外参数
    
    示例:
        >>> class MyPage(MangoWidget):
        >>>     def load_page_data(self):
        >>>         # 加载数据逻辑
        >>>         pass
        >>> 
        >>> page = MyPage(parent)
        >>> page.show_data()  # 异步加载数据
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.worker = None
        self.layout = MangoVBoxLayout()
        self.setLayout(self.layout)

    def show_data(self):
        """
        显示数据
        
        启动异步数据加载工作线程。如果已有线程正在运行，则不会启动新的线程。
        """
        if self.worker is not None and self.worker.isRunning():
            return
        self.worker = DataLoadWorker(self)
        self.worker.finished.connect(lambda: setattr(self, 'worker', None))
        self.worker.start()

    def load_page_data(self):
        """
        加载页面数据
        
        子类应重写此方法来实现具体的数据加载逻辑。
        此方法会在后台线程中执行，避免阻塞主界面。
        """
        pass
