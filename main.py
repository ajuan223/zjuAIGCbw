import sys
import yaml
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from uit import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.lock_model_combo)

    def lock_model_combo(self):
        self.comboBox_2.setEnabled(False)
        self.model_value = self.comboBox_2.currentText()
        # 选择参数和超参数文件路径及图片路径
        if self.model_value == "0":
            para_path = 'classify/train/para.txt'
            args_path = 'classify/train/args.yaml'
            img_path = 'classify/train/roc_curves.png'
        elif self.model_value == "1":
            para_path = 'classify/train2/para2.txt'
            args_path = 'classify/train2/args.yaml'
            img_path = 'classify/train2/roc_curves.png'
        else:
            para_path = 'classify/train3/para3.txt'
            args_path = 'classify/train3/args.yaml'
            img_path = 'classify/train3/roc_curves.png'
        # 读取并显示参数
        if para_path:
            try:
                with open(para_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    value = line.strip().split(':')[-1].strip()
                    self.tableWidget.setRowCount(4)
                    self.tableWidget.setColumnCount(1)
                    self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(value))
                self.textEdit.setPlainText(''.join(lines))
            except Exception as e:
                self.textEdit.setPlainText(f"读取参数文件失败: {e}")
        # 读取并显示超参数
        if args_path:
            try:
                with open(args_path, 'r', encoding='utf-8') as f:
                    args = yaml.safe_load(f)
                self.DoubleSpinBox.setValue(float(args.get('lr0', 0.01)))
                self.eprochSpinBox.setValue(int(args.get('epochs', 100)))
                self.batchSizeSpinBox.setValue(int(args.get('batch', 32)))
            except Exception as e:
                self.textEdit.append(f"\n读取超参数文件失败: {e}")
        # 显示图片
        if hasattr(self, 'roc_img_label'):
            self.roc_img_label.setParent(None)
        self.roc_img_label = QLabel(self.widget)
        self.roc_img_label.setGeometry(0, 0, 261, 201)
        pixmap = QPixmap(img_path)
        self.roc_img_label.setPixmap(pixmap.scaled(self.roc_img_label.size()))
        self.roc_img_label.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())