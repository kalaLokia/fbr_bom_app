# Form implementation generated from reading ui file '.\manage_price_structure.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(380, 440)
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(10, 200, 360, 201))
        self.listView.setObjectName("listView")
        self.text_filter = QtWidgets.QLineEdit(Form)
        self.text_filter.setGeometry(QtCore.QRect(10, 170, 360, 25))
        self.text_filter.setObjectName("text_filter")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 410, 320, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_save = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_4.addWidget(self.btn_save)
        self.btn_update = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout_4.addWidget(self.btn_update)
        self.btn_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout_4.addWidget(self.btn_delete)
        self.btn_close = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_4.addWidget(self.btn_close)
        self.layoutWidget_2 = QtWidgets.QWidget(Form)
        self.layoutWidget_2.setGeometry(QtCore.QRect(30, 120, 321, 27))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_3.setMinimumSize(QtCore.QSize(90, 0))
        self.label_3.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.text_basic = QtWidgets.QLineEdit(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_basic.sizePolicy().hasHeightForWidth())
        self.text_basic.setSizePolicy(sizePolicy)
        self.text_basic.setMinimumSize(QtCore.QSize(0, 25))
        self.text_basic.setObjectName("text_basic")
        self.horizontalLayout_3.addWidget(self.text_basic)
        self.layoutWidget_3 = QtWidgets.QWidget(Form)
        self.layoutWidget_3.setGeometry(QtCore.QRect(30, 70, 321, 27))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_2.setMinimumSize(QtCore.QSize(90, 0))
        self.label_2.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.text_mrp = QtWidgets.QLineEdit(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_mrp.sizePolicy().hasHeightForWidth())
        self.text_mrp.setSizePolicy(sizePolicy)
        self.text_mrp.setMinimumSize(QtCore.QSize(0, 25))
        self.text_mrp.setObjectName("text_mrp")
        self.horizontalLayout_2.addWidget(self.text_mrp)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 150, 47, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label_4.setObjectName("label_4")
        self.layoutWidget_4 = QtWidgets.QWidget(Form)
        self.layoutWidget_4.setGeometry(QtCore.QRect(30, 20, 321, 27))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(90, 0))
        self.label.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.combo_structure = QtWidgets.QComboBox(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.combo_structure.setFont(font)
        self.combo_structure.setObjectName("combo_structure")
        self.combo_structure.addItem("")
        self.combo_structure.addItem("")
        self.combo_structure.addItem("")
        self.horizontalLayout.addWidget(self.combo_structure)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_save.setText(_translate("Form", "Save"))
        self.btn_update.setText(_translate("Form", "Update"))
        self.btn_delete.setText(_translate("Form", "Delete"))
        self.btn_close.setText(_translate("Form", "Close"))
        self.label_3.setText(_translate("Form", "BASIC"))
        self.label_2.setText(_translate("Form", "MRP"))
        self.label_4.setText(_translate("Form", "Filter"))
        self.label.setText(_translate("Form", "Structure"))
        self.combo_structure.setItemText(0, _translate("Form", "Pride"))
        self.combo_structure.setItemText(1, _translate("Form", "Debongo"))
        self.combo_structure.setItemText(2, _translate("Form", "Stile"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())