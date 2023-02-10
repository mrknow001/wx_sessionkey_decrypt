from UI import *
from functools import partial
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from WX_login_crypt import *
import urllib.parse


class MainWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        try:
            reply = QtWidgets.QMessageBox.question(self,'提醒',"是否要退出程序？",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
                print("主窗口已关闭")
            else:
                event.ignore()
        except Exception as e:
            print(e)

def show_message(ui,msg):
    QtWidgets.QMessageBox.information(ui.pushButton, "提示", msg)

def write_textEdit(ui, data):
    ui.textEdit.clear()
    ui.textEdit.setText(data)

def write_textEdit_2(ui, data):
    ui.textEdit_2.clear()
    ui.textEdit_2.setText(data)

def En_url(ui):
    ui.textEdit_2.setText(urllib.parse.quote(ui.textEdit_2.toPlainText().strip()))

def Dn_url(ui):
    ui.textEdit_2.setText(urllib.parse.unquote(ui.textEdit_2.toPlainText().strip()))


def key_function(ui):


    class En_MyThread(QThread):
        my_signal = pyqtSignal(object, str)
        def __init__(self):
            super().__init__()

        def run(self):
            key = ui.lineEdit.text()
            iv = ui.lineEdit_2.text()
            decrypted_data = ui.textEdit.toPlainText().strip()
            result = encrypt_data(decrypted_data, iv, key)
            if result is not None:
                try:
                    self.my_signal.emit(ui, result)
                except Exception as e:
                    print(e)

    class De_MyThread(QThread):
        my_signal = pyqtSignal(object, str)
        def __init__(self):
            super().__init__()

        def run(self):
            key = ui.lineEdit.text()
            iv = ui.lineEdit_2.text()
            decrypted_data = ui.textEdit_2.toPlainText().strip()
            result = decrypt_data(decrypted_data, iv, key)
            if result is not None:
                try:
                    self.my_signal.emit(ui, result)
                except Exception as e:
                    print(e)

    class BatchEn_MyThread(QThread):
        my_signal = pyqtSignal(object, str)
        def __init__(self):
            super().__init__()

        def run(self):
            key = ui.lineEdit.text()
            iv = ui.lineEdit_2.text()
            original = ui.textEdit.toPlainText().strip()
            decrypted_data = ui.textEdit_2.toPlainText().strip()
            datas = decrypted_data.split("\n")
            new_datas = []
            for data in datas:
                new_datas.append(original.replace("%%",data))
            result = Batch_En(new_datas,iv,key)
            if result is not None:
                try:
                    self.my_signal.emit(ui, result)
                except Exception as e:
                    print(e)

    En_MyThread = En_MyThread()
    De_MyThread = De_MyThread()
    BatchEn_MyThread = BatchEn_MyThread()
    En_MyThread.my_signal.connect(write_textEdit_2)
    De_MyThread.my_signal.connect(write_textEdit)
    BatchEn_MyThread.my_signal.connect(write_textEdit_2)
    ui.pushButton.clicked.connect(partial(En_MyThread.start))
    ui.pushButton_2.clicked.connect(partial(De_MyThread.start))
    ui.pushButton_3.clicked.connect(partial(BatchEn_MyThread.start))
    ui.pushButton_4.clicked.connect(partial(En_url, ui))
    ui.pushButton_5.clicked.connect(partial(Dn_url, ui))


if __name__ == "__main__":
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)# 解决高分辨率问题（网上搜的，暂未发现，如果发现有问题可以试试这条）
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    Ui_C = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.setWindowTitle("微信一键登录解密")
    # widget.setWindowIcon(QtGui.QIcon(":/logo.png"))
    widget.show()
    key_function(ui)
    sys.exit(app.exec_())
