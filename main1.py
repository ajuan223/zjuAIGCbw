import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class DataThread(QThread):
    dataSignal = pyqtSignal(str)

    def run(self):
        # 模拟耗时数据读取
        for i in range(5):
            time.sleep(2)  # 假设每2秒读取一条数据
            self.dataSignal.emit(f"数据 {i+1}")
        self.dataSignal.emit("读取完成")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("等待数据...", self)
        self.button = QPushButton("开始读取", self)
        self.button.clicked.connect(self.start_thread)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.thread = None
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.stop_thread)

    def start_thread(self):
        self.label.setText("开始读取数据...")
        self.thread = DataThread()
        self.thread.dataSignal.connect(self.show_data)
        self.thread.start()
        self.timer.start(10000)  # 10秒计时

    def show_data(self, msg):
        self.label.setText(msg)
        if msg == "读取完成":
            self.timer.stop()

    def stop_thread(self):
        if self.thread and self.thread.isRunning():
            self.thread.terminate()
            self.label.setText("10秒超时，线程已终止")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())