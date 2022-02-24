import os
import threading

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from database.create_data_tables import createBomArticleTable


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(440, 240)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 30, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 200, 331, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 210, 411, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(20, 180, 150, 16))
        self.label_5.setObjectName("label_5")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 170, 481, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget = QtWidgets.QWidget(Form)
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
        self.btn_update = QtWidgets.QPushButton(Form)
        self.btn_update.setGeometry(QtCore.QRect(250, 140, 75, 26))
        self.btn_update.setMaximumSize(QtCore.QSize(16777215, 28))
        self.btn_update.setObjectName("btn_update")
        self.btn_close = QtWidgets.QPushButton(Form)
        self.btn_close.setGeometry(QtCore.QRect(340, 140, 75, 26))
        self.btn_close.setMaximumSize(QtCore.QSize(16777215, 28))
        self.btn_close.setObjectName("btn_close")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(230, 10, 171, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.layoutWidget1 = QtWidgets.QWidget(Form)
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
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # Setting progress bar in hidden state initially
        self.progressBar.hide()
        self.btn_choose_bom.clicked.connect(self.getBomFile)
        self.btn_choose_materials.clicked.connect(self.getMaterialsFile)
        self.btn_update.clicked.connect(self.updateTables)
        self.btn_close.clicked.connect(
            lambda: QtCore.QCoreApplication.instance().quit()
        )

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Bom heirarchy"))
        self.label_2.setText(_translate("Form", "Item master data"))
        self.label_3.setText(
            _translate(
                "Form",
                "BOM: father, father name, child, child qty, process, process order",
            )
        )
        self.label_4.setText(
            _translate(
                "Form",
                "ITEM: item no, mrp, foreign name, no of pairs, product type, inventory uom, last purchase price",
            )
        )
        self.label_5.setText(_translate("Form", "Mandatory column names"))
        self.btn_choose_bom.setText(_translate("Form", "..."))
        self.btn_update.setText(_translate("Form", "Update"))
        self.btn_close.setText(_translate("Form", "Close"))
        self.btn_choose_materials.setText(_translate("Form", "..."))

    def getBomFile(self):
        """Opens file dialog for choosing Bom file"""

        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open File", "./data", "Excel Files (*.xlsx)"
        )
        self.text_bom_path.setText(filename[0])

    def getMaterialsFile(self):
        """Opens file dialog for choosing Materials file"""

        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open File", "./data", "Excel Files (*.xlsx)"
        )
        self.text_materials_path.setText(filename[0])

    # def closeWindow(self):
    #     """Close the current dialog window."""

    #     QtCore.QCoreApplication.instance().quit()

    def updateTables(self):
        """Update bom, article list tables."""

        bom_path = self.text_bom_path.text()
        materials_path = self.text_materials_path.text()

        if not os.path.exists(bom_path):
            print("Invalid path given for bom file.")
            return
        if not os.path.exists(materials_path):
            print("Invalid path given for materials file.")
            return

        self.progressBar.setStyleSheet(
            "QProgressBar::chunk{background-color:#16b1cc;margin:1px}QProgressBar{text-align:center;border-radius: 2px;border: 1px solid #16b1cc;}"
        )
        self.progressBar.show()
        self.progressBar.setProperty("value", 1)

        # TODO: Get a callback when thread finished to show a dialog.
        thread = threading.Thread(
            target=createBomArticleTable,
            args=(
                bom_path,
                materials_path,
                self,
            ),
        )
        thread.daemon = True
        thread.start()
        # self.success_dialog()

    def success_dialog(self):
        """Shows successful message"""
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowIcon(QtGui.QIcon("icons/gear-solid.svg"))
        dialog.setWindowTitle("Updated Successfully")
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
        dialog.setText("Articles and Bom tables has been re created successfully.")
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        retval = dialog.exec()
        print(retval)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
