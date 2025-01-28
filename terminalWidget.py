# -*- encoding: utf-8 -*-
'''
@Time    :   2025/01/13 20:44:43
@File    :   parameterWidget.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   0.1.0
@Contact :   for_freedom_x64@live.com
'''

import sys, subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QLineEdit
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QKeySequence, QShortcut


class CommandRunner(QThread):
    """线程类，用于执行命令并实时返回输出。"""
    output_signal = Signal(str)  # 信号，用于发送输出到主线程

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.running = True  # 标记线程是否应继续运行

    def run(self):
        """运行命令并读取实时输出。"""
        try:
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            while self.running:
                # 从标准输出和错误输出中逐行读取
                output = process.stdout.readline()
                if output:
                    self.output_signal.emit(output.strip())  # 发送标准输出
                if process.poll() is not None:
                    break

            # 读取剩余的输出
            for remaining_output in process.stdout.readlines():
                self.output_signal.emit(remaining_output.strip())

            for remaining_error in process.stderr.readlines():
                self.output_signal.emit(remaining_error.strip())
        except Exception as e:
            self.output_signal.emit(f"Error: {e}")

    def stop(self):
        """停止线程的运行。"""
        self.running = False
        self.quit()


class TerminalWidget(QMainWindow):
    signalQuit = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Embedded Terminal with Real-Time Output")
        self.resize(800, 600)

        # 创建一个 QPlainTextEdit 作为终端输出窗口
        self.output_console = QPlainTextEdit(self)
        self.output_console.setReadOnly(True)  # 设置只读
        self.output_console.setStyleSheet('font-family: "Helvetica Neue","Meslo LG M for Powerline", Arial, sans-serif; font-size: 12px;')
        shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        shortcut.activated.connect(self.close)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.output_console)
        # layout.addWidget(self.command_input)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStyleSheet('QPlainTextEdit{border: 1px solid #919191;border-radius: 3px;color:#dbdbdb;margin:0px;background-color:#031c0a} TerminalWidget{margin:0px;padding:0px;background-color:#1d1d1d}')

        # 线程对象
        self.command_thread = None

    def runCommand(self, command):
        """运行用户输入的命令，并实时显示输出。"""
        # command = self.command_input.text().strip()
        if not command:
            return

        # 显示用户输入的命令
        self.output_console.appendPlainText(f"> {command}")
        # self.command_input.clear()

        # 如果已有线程在运行，先停止
        if self.command_thread and self.command_thread.isRunning():
            self.command_thread.stop()

        # 创建新的命令线程
        self.command_thread = CommandRunner(command)
        self.command_thread.output_signal.connect(self.display_output)  # 绑定输出信号
        self.command_thread.start()

    def display_output(self, text):
        """显示命令输出到 QPlainTextEdit。"""
        self.output_console.appendPlainText(text)

    def closeEvent(self, event):
        self.signalQuit.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TerminalWidget()
    window.runCommand('ping www.baidu.com')
    window.show()
    sys.exit(app.exec())
