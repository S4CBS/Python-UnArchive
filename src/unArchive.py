import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.path = None
        self.unpath = None
        self.actions = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("arch.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget.setBaseSize(QtCore.QSize(800, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.ArchivePath = QtWidgets.QPushButton(self.centralwidget)
        self.ArchivePath.setGeometry(QtCore.QRect(20, 32, 141, 31))
        self.ArchivePath.setStyleSheet(open(os.path.join('css', 'osn.css')).read())
        self.ArchivePath.setObjectName("ArchivePath")

        self.ArchivePath.clicked.connect(self.forArchivePath)

        self.lineEditOsn = QtWidgets.QTextEdit(self.centralwidget)
        self.lineEditOsn.setGeometry(QtCore.QRect(170, 30, 591, 511))
        self.lineEditOsn.setStyleSheet("border-color: rgb(255, 0, 0);\n"
                                       "color: rgb(96, 255, 255);\n"
                                       "background-color: rgb(127, 127, 127);")
        self.lineEditOsn.setObjectName("lineEditOsn")
        self.UnArchivePath = QtWidgets.QPushButton(self.centralwidget)
        self.UnArchivePath.setGeometry(QtCore.QRect(20, 70, 141, 41))
        self.UnArchivePath.setStyleSheet(open(os.path.join('css', 'osn.css')).read())
        self.UnArchivePath.setObjectName("UnArchivePath")
        self.UnArchiveBut = QtWidgets.QPushButton(self.centralwidget)
        self.UnArchiveBut.setGeometry(QtCore.QRect(20, 120, 141, 31))
        self.UnArchiveBut.setStyleSheet(open(os.path.join('css', 'osn.css')).read())
        self.UnArchiveBut.setObjectName("UnArchiveBut")

        self.UnArchivePath.clicked.connect(self.forUnArchivePath)
        self.UnArchiveBut.clicked.connect(self.UnArchive)

        self.ExitBut = QtWidgets.QPushButton(self.centralwidget)
        self.ExitBut.setGeometry(QtCore.QRect(20, 550, 141, 31))
        self.ExitBut.setStyleSheet(open(os.path.join('css', 'osn.css')).read())
        self.ExitBut.setObjectName("ExitBut")

        self.ExitBut.clicked.connect(self.exit)

        self.lineEditS4CBS = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditS4CBS.setGeometry(QtCore.QRect(170, 550, 591, 31))
        self.lineEditS4CBS.setToolTip("")
        self.lineEditS4CBS.setStyleSheet("border-color: rgb(255, 0, 0);\n"
                                         "color: rgb(96, 255, 255);\n"
                                         "background-color: rgb(127, 127, 127);")
        self.lineEditS4CBS.setObjectName("lineEditS4CBS")
        self.InfoBut = QtWidgets.QPushButton(self.centralwidget)
        self.InfoBut.setGeometry(QtCore.QRect(20, 510, 141, 31))
        self.InfoBut.setStyleSheet(open(os.path.join('css', 'osn.css')).read())
        self.InfoBut.setObjectName("InfoBut")

        self.InfoBut.clicked.connect(self.show_info_dialog)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UnArchive"))
        self.ArchivePath.setText(_translate("MainWindow", "Выбирите файл архива"))
        self.UnArchivePath.setText(_translate("MainWindow", "Выбирите папку\n"
                                              "куда распаковать архив"))
        self.UnArchiveBut.setText(_translate("MainWindow", "Начать распаковку"))
        self.ExitBut.setText(_translate("MainWindow", "Выйти"))
        self.lineEditS4CBS.setText(_translate("MainWindow", "                                                                           https://github.com/S4CBS"))
        self.InfoBut.setText(_translate("MainWindow", "Информация"))

    def forArchivePath(self):
        from tkinter import filedialog

        self.path = filedialog.askopenfilename()
        self.path = self.path.replace('/', '\\')

        self.actions.append(f'Selected Archive Path: {self.path}')
        self.updateLineEdit()
        
    def forUnArchivePath(self):
        from tkinter import filedialog
        from tkinter import messagebox

        if self.path == '' or self.path is None:
                messagebox.showerror(title='Ошибка!', message='Выбирете сначала файл архива!')
        else:
                self.unpath = filedialog.askdirectory()
                self.unpath = self.unpath.replace('/', '\\')

                self.actions.append(f'Selected UnArchive Path: {self.unpath}')
                self.updateLineEdit()
        
    def UnArchive(self):
        from tkinter import messagebox
        import rarfile
        import zipfile
        from zipfile import BadZipFile

        if self.path == '' or self.path is None or self.unpath == '' or self.unpath is None:
            messagebox.showerror(title='Ошибка!', message='Выбирете сначала файл архива и путь куда распаковать архив!')
        else:
            try:
                single = self.check(10)

                os.mkdir(os.path.join(self.unpath, f'UnArchive-{single}'))
                self.unpath = os.path.join(self.unpath, f'UnArchive-{single}')
                
                with zipfile.ZipFile(self.path, 'r') as ref:
                    ref.extractall(self.unpath)

                self.actions.append(f'UnArchived to: {self.unpath}')
                self.updateLineEdit()

                messagebox.showinfo(title='Успешно!', message=f'Файл {self.unpath} успешно распакован!')
            except BadZipFile:
                try:
                    unrar_exe_path = 'UnRAR.exe'
                    os.environ['RAR_CMD'] = unrar_exe_path

                    with rarfile.RarFile(self.path, 'r') as rf:
                        rf.extractall(self.unpath)

                    self.actions.append(f'UnArchived to: {self.unpath}')
                    self.updateLineEdit()

                    messagebox.showinfo(title='Успешно!', message=f'Файл {self.unpath} успешно распакован!')
                except Exception as e:
                    messagebox.showerror(title='Ошибка!', message=f'Ошибка при распаковке RAR архива: {e}')

    def exit(self):
        self.actions.append('Application Exit')
        self.updateLineEdit()
        sys.exit()

    def updateLineEdit(self):
        text = '\n'.join(self.actions)
        self.lineEditOsn.setPlainText(text)
        cursor = self.lineEditOsn.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.lineEditOsn.setTextCursor(cursor)

    def check(self,length):
         import string
         import random
         return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def show_info_dialog(self):
        from about.about import AboutDialog

        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def open_s4cbs_website(self, link):
        QDesktopServices.openUrl(QUrl(link))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
