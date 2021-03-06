from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogManagePS(object):
    def setupUi(self, DialogManagePS):
        DialogManagePS.setObjectName("DialogManagePS")
        DialogManagePS.resize(380, 451)
        self.tv_filter_box = QtWidgets.QTableView(DialogManagePS)
        self.tv_filter_box.setGeometry(QtCore.QRect(10, 200, 360, 201))
        self.tv_filter_box.setObjectName("tv_filter_box")
        self.text_filter = QtWidgets.QLineEdit(DialogManagePS)
        self.text_filter.setGeometry(QtCore.QRect(10, 170, 321, 25))
        self.text_filter.setObjectName("text_filter")
        self.layoutWidget = QtWidgets.QWidget(DialogManagePS)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 410, 320, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_save = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_save.setEnabled(False)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_4.addWidget(self.btn_save)
        self.btn_update = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_update.setEnabled(False)
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout_4.addWidget(self.btn_update)
        self.btn_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_delete.setEnabled(False)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout_4.addWidget(self.btn_delete)
        self.btn_close = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_4.addWidget(self.btn_close)
        self.layoutWidget_2 = QtWidgets.QWidget(DialogManagePS)
        self.layoutWidget_2.setGeometry(QtCore.QRect(30, 120, 321, 27))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_basic = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_basic.setMinimumSize(QtCore.QSize(90, 0))
        self.label_basic.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_basic.setFont(font)
        self.label_basic.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_basic.setObjectName("label_basic")
        self.horizontalLayout_3.addWidget(self.label_basic)
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
        self.layoutWidget_3 = QtWidgets.QWidget(DialogManagePS)
        self.layoutWidget_3.setGeometry(QtCore.QRect(30, 70, 321, 27))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_mrp = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_mrp.setMinimumSize(QtCore.QSize(90, 0))
        self.label_mrp.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_mrp.setFont(font)
        self.label_mrp.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_mrp.setObjectName("label_mrp")
        self.horizontalLayout_2.addWidget(self.label_mrp)
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
        self.label_filter = QtWidgets.QLabel(DialogManagePS)
        self.label_filter.setGeometry(QtCore.QRect(10, 150, 47, 16))
        self.label_filter.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label_filter.setObjectName("label_filter")
        self.layoutWidget_4 = QtWidgets.QWidget(DialogManagePS)
        self.layoutWidget_4.setGeometry(QtCore.QRect(30, 20, 321, 27))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_structure = QtWidgets.QLabel(self.layoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_structure.sizePolicy().hasHeightForWidth())
        self.label_structure.setSizePolicy(sizePolicy)
        self.label_structure.setMinimumSize(QtCore.QSize(90, 0))
        self.label_structure.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_structure.setFont(font)
        self.label_structure.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_structure.setObjectName("label_structure")
        self.horizontalLayout.addWidget(self.label_structure)
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
        self.btn_export_all = QtWidgets.QPushButton(DialogManagePS)
        self.btn_export_all.setGeometry(QtCore.QRect(340, 170, 31, 25))
        self.btn_export_all.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\../icons/file-export-solid.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_export_all.setIcon(icon)
        self.btn_export_all.setObjectName("btn_export_all")

        self.retranslateUi(DialogManagePS)
        QtCore.QMetaObject.connectSlotsByName(DialogManagePS)
        DialogManagePS.setTabOrder(self.combo_structure, self.text_mrp)
        DialogManagePS.setTabOrder(self.text_mrp, self.text_basic)
        DialogManagePS.setTabOrder(self.text_basic, self.text_filter)
        DialogManagePS.setTabOrder(self.text_filter, self.btn_save)
        DialogManagePS.setTabOrder(self.btn_save, self.btn_update)
        DialogManagePS.setTabOrder(self.btn_update, self.btn_delete)
        DialogManagePS.setTabOrder(self.btn_delete, self.btn_close)
        DialogManagePS.setTabOrder(self.btn_close, self.tv_filter_box)

    def retranslateUi(self, DialogManagePS):
        _translate = QtCore.QCoreApplication.translate
        DialogManagePS.setWindowTitle(_translate("DialogManagePS", "Manage Price Structure"))
        self.btn_save.setText(_translate("DialogManagePS", "Save"))
        self.btn_update.setText(_translate("DialogManagePS", "Update"))
        self.btn_delete.setText(_translate("DialogManagePS", "Delete"))
        self.btn_close.setText(_translate("DialogManagePS", "Close"))
        self.label_basic.setText(_translate("DialogManagePS", "BASIC"))
        self.label_mrp.setText(_translate("DialogManagePS", "MRP"))
        self.label_filter.setText(_translate("DialogManagePS", "Filter"))
        self.label_structure.setText(_translate("DialogManagePS", "Structure"))
        self.combo_structure.setItemText(0, _translate("DialogManagePS", "Pride"))
        self.combo_structure.setItemText(1, _translate("DialogManagePS", "Debongo"))
        self.combo_structure.setItemText(2, _translate("DialogManagePS", "Stile"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogManagePS = QtWidgets.QWidget()
    ui = Ui_DialogManagePS()
    ui.setupUi(DialogManagePS)
    DialogManagePS.show()
    sys.exit(app.exec())
