from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogCreateBom(object):
    def setupUi(self, DialogCreateBom):
        DialogCreateBom.setObjectName("DialogCreateBom")
        DialogCreateBom.resize(440, 240)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("icons:gear-solid.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        DialogCreateBom.setWindowIcon(icon)
        self.label_path_1 = QtWidgets.QLabel(DialogCreateBom)
        self.label_path_1.setGeometry(QtCore.QRect(20, 30, 111, 16))
        self.label_path_1.setObjectName("label_path_1")
        self.label_path_2 = QtWidgets.QLabel(DialogCreateBom)
        self.label_path_2.setGeometry(QtCore.QRect(20, 80, 141, 16))
        self.label_path_2.setObjectName("label_path_2")
        self.label_info_cols_1 = QtWidgets.QLabel(DialogCreateBom)
        self.label_info_cols_1.setGeometry(QtCore.QRect(20, 200, 331, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_info_cols_1.setFont(font)
        self.label_info_cols_1.setObjectName("label_info_cols_1")
        self.label_info_cols_2 = QtWidgets.QLabel(DialogCreateBom)
        self.label_info_cols_2.setGeometry(QtCore.QRect(20, 210, 411, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_info_cols_2.setFont(font)
        self.label_info_cols_2.setObjectName("label_info_cols_2")
        self.label_info_cols_head = QtWidgets.QLabel(DialogCreateBom)
        self.label_info_cols_head.setGeometry(QtCore.QRect(20, 180, 211, 16))
        self.label_info_cols_head.setObjectName("label_info_cols_head")
        self.line = QtWidgets.QFrame(DialogCreateBom)
        self.line.setGeometry(QtCore.QRect(0, 170, 481, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget = QtWidgets.QWidget(DialogCreateBom)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 50, 401, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.text_bom_path = QtWidgets.QLineEdit(self.layoutWidget)
        self.text_bom_path.setObjectName("text_bom_path")
        self.horizontalLayout_2.addWidget(self.text_bom_path)
        self.btn_choose_bom = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_choose_bom.setMaximumSize(QtCore.QSize(25, 24))
        self.btn_choose_bom.setObjectName("btn_choose_bom")
        self.horizontalLayout_2.addWidget(self.btn_choose_bom)
        self.btn_update = QtWidgets.QPushButton(DialogCreateBom)
        self.btn_update.setGeometry(QtCore.QRect(250, 140, 75, 26))
        self.btn_update.setMaximumSize(QtCore.QSize(16777215, 28))
        self.btn_update.setObjectName("btn_update")
        self.btn_close = QtWidgets.QPushButton(DialogCreateBom)
        self.btn_close.setGeometry(QtCore.QRect(340, 140, 75, 26))
        self.btn_close.setMaximumSize(QtCore.QSize(16777215, 28))
        self.btn_close.setObjectName("btn_close")
        self.progressBar = QtWidgets.QProgressBar(DialogCreateBom)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(230, 10, 171, 23))
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.layoutWidget1 = QtWidgets.QWidget(DialogCreateBom)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 100, 401, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.text_materials_path = QtWidgets.QLineEdit(self.layoutWidget1)
        self.text_materials_path.setObjectName("text_materials_path")
        self.horizontalLayout.addWidget(self.text_materials_path)
        self.btn_choose_materials = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_choose_materials.setMaximumSize(QtCore.QSize(25, 24))
        self.btn_choose_materials.setObjectName("btn_choose_materials")
        self.horizontalLayout.addWidget(self.btn_choose_materials)

        self.retranslateUi(DialogCreateBom)
        QtCore.QMetaObject.connectSlotsByName(DialogCreateBom)

    def retranslateUi(self, DialogCreateBom):
        _translate = QtCore.QCoreApplication.translate
        DialogCreateBom.setWindowTitle(
            _translate("DialogCreateBom", "Update Bom Table")
        )
        self.label_path_1.setText(_translate("DialogCreateBom", "Bom heirarchy"))
        self.label_path_2.setText(_translate("DialogCreateBom", "Item master data"))
        self.label_info_cols_1.setText(
            _translate(
                "DialogCreateBom",
                "BOM: father, father name, child, child qty, process, process order",
            )
        )
        self.label_info_cols_2.setText(
            _translate(
                "DialogCreateBom",
                "ITEM: item no, mrp, foreign name, no of pairs, product type, inventory uom, last purchase price",
            )
        )
        self.label_info_cols_head.setText(
            _translate("DialogCreateBom", "Mandatory column names")
        )
        self.btn_choose_bom.setText(_translate("DialogCreateBom", "..."))
        self.btn_update.setText(_translate("DialogCreateBom", "Update"))
        self.btn_close.setText(_translate("DialogCreateBom", "Close"))
        self.btn_choose_materials.setText(_translate("DialogCreateBom", "..."))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    DialogCreateBom = QtWidgets.QWidget()
    ui = Ui_DialogCreateBom()
    ui.setupUi(DialogCreateBom)
    DialogCreateBom.show()
    sys.exit(app.exec())
