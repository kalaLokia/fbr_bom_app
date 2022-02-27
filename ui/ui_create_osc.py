from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogUpdateFromFile(object):
    def setupUi(self, DialogUpdateFromFile):
        DialogUpdateFromFile.setObjectName("DialogUpdateFromFile")
        DialogUpdateFromFile.resize(480, 171)
        self.layoutWidget = QtWidgets.QWidget(DialogUpdateFromFile)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 40, 401, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.text_file_path = QtWidgets.QLineEdit(self.layoutWidget)
        self.text_file_path.setObjectName("text_file_path")
        self.horizontalLayout_2.addWidget(self.text_file_path)
        self.btn_choose_file = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_choose_file.setMaximumSize(QtCore.QSize(25, 24))
        self.btn_choose_file.setObjectName("btn_choose_file")
        self.horizontalLayout_2.addWidget(self.btn_choose_file)
        self.label_item = QtWidgets.QLabel(DialogUpdateFromFile)
        self.label_item.setGeometry(QtCore.QRect(30, 20, 181, 16))
        self.label_item.setObjectName("label_item")
        self.btn_update = QtWidgets.QPushButton(DialogUpdateFromFile)
        self.btn_update.setGeometry(QtCore.QRect(270, 80, 75, 26))
        self.btn_update.setMaximumSize(QtCore.QSize(16777215, 28))
        self.btn_update.setObjectName("btn_update")
        self.btn_close = QtWidgets.QPushButton(DialogUpdateFromFile)
        self.btn_close.setGeometry(QtCore.QRect(360, 80, 75, 26))
        self.btn_close.setMaximumSize(QtCore.QSize(16777215, 28))
        self.btn_close.setObjectName("btn_close")
        self.line = QtWidgets.QFrame(DialogUpdateFromFile)
        self.line.setGeometry(QtCore.QRect(0, 120, 481, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.label_info = QtWidgets.QLabel(DialogUpdateFromFile)
        self.label_info.setGeometry(QtCore.QRect(20, 140, 391, 16))
        self.label_info.setObjectName("label_info")

        self.retranslateUi(DialogUpdateFromFile)
        QtCore.QMetaObject.connectSlotsByName(DialogUpdateFromFile)

    def retranslateUi(self, DialogUpdateFromFile):
        _translate = QtCore.QCoreApplication.translate
        DialogUpdateFromFile.setWindowTitle(
            _translate("DialogUpdateFromFile", "Update OS Charges")
        )
        self.btn_choose_file.setText(_translate("DialogUpdateFromFile", "..."))
        self.label_item.setText(_translate("DialogUpdateFromFile", "Choose file:"))
        self.btn_update.setText(_translate("DialogUpdateFromFile", "Update"))
        self.btn_close.setText(_translate("DialogUpdateFromFile", "Close"))
        self.label_info.setText(
            _translate(
                "DialogUpdateFromFile",
                "Column names: article, stitching, printing  (article format: 0000-BK-G)",
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    DialogUpdateFromFile = QtWidgets.QWidget()
    ui = Ui_DialogUpdateFromFile()
    ui.setupUi(DialogUpdateFromFile)
    DialogUpdateFromFile.show()
    sys.exit(app.exec())
