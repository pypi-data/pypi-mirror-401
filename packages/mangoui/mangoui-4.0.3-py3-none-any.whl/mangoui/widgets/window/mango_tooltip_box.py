# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 消息框工具函数 - 提供统一的消息提示框样式
# @Time   : 2024-05-27 13:04
# @Author : 毛鹏
from PySide6.QtWidgets import QMessageBox

from mangoui.settings.settings import THEME


def show_failed_message(text: str, title: str = '失败'):
    """
    显示失败消息框
    
    显示一个带有错误图标的消息框，用于提示操作失败。
    
    参数:
        text: 消息文本
        title: 消息框标题，默认 "失败"
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)  # type: ignore
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStyleSheet(f"""
        QMessageBox {{
            background-color: {THEME.bg_100};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}
        QPushButton {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            padding: 5px 15px;
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}
        QPushButton:hover {{
            background-color: {THEME.primary_200};
        }}
    """)
    msg.exec()


def show_success_message(text: str, title: str = '成功'):
    """
    显示成功消息框
    
    显示一个带有信息图标的消息框，用于提示操作成功。
    
    参数:
        text: 消息文本
        title: 消息框标题，默认 "成功"
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)  # type: ignore
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStyleSheet(f"""
        QMessageBox {{
            background-color: {THEME.bg_100};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}
        QPushButton {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            padding: 5px 15px;
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}
        QPushButton:hover {{
            background-color: {THEME.primary_200};
        }}
    """)
    msg.exec()


def show_warning_message(text: str, title: str = '警告'):
    """
    显示警告消息框
    
    显示一个带有警告图标的消息框，用于提示警告信息。
    
    参数:
        text: 消息文本
        title: 消息框标题，默认 "警告"
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)  # type: ignore
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStyleSheet(f"""
        QMessageBox {{
            background-color: {THEME.bg_100};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}
        QPushButton {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            padding: 5px 15px;
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}
        QPushButton:hover {{
            background-color: {THEME.primary_200};
        }}
    """)
    msg.exec()


def show_info_message(text: str, title: str = '提示'):
    """
    显示信息消息框
    
    显示一个带有信息图标的消息框，用于提示一般信息。
    
    参数:
        text: 消息文本
        title: 消息框标题，默认 "提示"
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)  # type: ignore
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStyleSheet(f"""
        QMessageBox {{
            background-color: {THEME.bg_100};
            color: {THEME.text_100};
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}
        QPushButton {{
            background-color: {THEME.primary_100};
            color: {THEME.bg_100};
            border-radius: {THEME.border_radius};
            padding: 5px 15px;
            font-family: {THEME.font.family};
            font-size: {THEME.font.text_size}px;
        }}
        QPushButton:hover {{
            background-color: {THEME.primary_200};
        }}
    """)
    msg.exec()