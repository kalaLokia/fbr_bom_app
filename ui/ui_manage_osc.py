from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogManageOSC(object):
    def setupUi(self, DialogManageOSC):
        DialogManageOSC.setObjectName("DialogManageOSC")
        DialogManageOSC.resize(380, 450)
        self.tv_filter_box = QtWidgets.QTableView(DialogManageOSC)
        self.tv_filter_box.setGeometry(QtCore.QRect(10, 200, 360, 201))
        self.tv_filter_box.setObjectName("tv_filter_box")
        self.text_filter = QtWidgets.QLineEdit(DialogManageOSC)
        self.text_filter.setGeometry(QtCore.QRect(10, 170, 360, 25))
        self.text_filter.setObjectName("text_filter")
        self.layoutWidget = QtWidgets.QWidget(DialogManageOSC)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 70, 321, 27))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_print = QtWidgets.QLabel(self.layoutWidget)
        self.label_print.setMinimumSize(QtCore.QSize(90, 0))
        self.label_print.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_print.setFont(font)
        self.label_print.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_print.setObjectName("label_print")
        self.horizontalLayout_2.addWidget(self.label_print)
        spacerItem = QtWidgets.QSpacerItem(
            10,
            20,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_2.addItem(spacerItem)
        self.text_print_rate = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.text_print_rate.sizePolicy().hasHeightForWidth()
        )
        self.text_print_rate.setSizePolicy(sizePolicy)
        self.text_print_rate.setMinimumSize(QtCore.QSize(0, 25))
        self.text_print_rate.setObjectName("text_print_rate")
        self.horizontalLayout_2.addWidget(self.text_print_rate)
        self.layoutWidget_2 = QtWidgets.QWidget(DialogManageOSC)
        self.layoutWidget_2.setGeometry(QtCore.QRect(30, 120, 321, 27))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_stitch = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_stitch.setMinimumSize(QtCore.QSize(90, 0))
        self.label_stitch.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_stitch.setFont(font)
        self.label_stitch.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_stitch.setObjectName("label_stitch")
        self.horizontalLayout_3.addWidget(self.label_stitch)
        spacerItem1 = QtWidgets.QSpacerItem(
            10,
            20,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_3.addItem(spacerItem1)
        self.text_stitch_rate = QtWidgets.QLineEdit(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.text_stitch_rate.sizePolicy().hasHeightForWidth()
        )
        self.text_stitch_rate.setSizePolicy(sizePolicy)
        self.text_stitch_rate.setMinimumSize(QtCore.QSize(0, 25))
        self.text_stitch_rate.setObjectName("text_stitch_rate")
        self.horizontalLayout_3.addWidget(self.text_stitch_rate)
        self.label_4 = QtWidgets.QLabel(DialogManageOSC)
        self.label_4.setGeometry(QtCore.QRect(10, 150, 47, 16))
        self.label_4.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(DialogManageOSC)
        self.label_5.setGeometry(QtCore.QRect(280, 50, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_5.setFont(font)
        self.label_5.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.label_5.setObjectName("label_5")
        self.layoutWidget1 = QtWidgets.QWidget(DialogManageOSC)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 20, 321, 27))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_article = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_article.sizePolicy().hasHeightForWidth()
        )
        self.label_article.setSizePolicy(sizePolicy)
        self.label_article.setMinimumSize(QtCore.QSize(90, 0))
        self.label_article.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_article.setFont(font)
        self.label_article.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_article.setObjectName("label_article")
        self.horizontalLayout.addWidget(self.label_article)
        spacerItem2 = QtWidgets.QSpacerItem(
            10,
            20,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem2)
        self.text_article = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_article.sizePolicy().hasHeightForWidth())
        self.text_article.setSizePolicy(sizePolicy)
        self.text_article.setMinimumSize(QtCore.QSize(0, 25))
        self.text_article.setObjectName("text_article")
        self.horizontalLayout.addWidget(self.text_article)
        self.layoutWidget2 = QtWidgets.QWidget(DialogManageOSC)
        self.layoutWidget2.setGeometry(QtCore.QRect(30, 410, 320, 25))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_save = QtWidgets.QPushButton(self.layoutWidget2)
        self.btn_save.setEnabled(False)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_4.addWidget(self.btn_save)
        self.btn_update = QtWidgets.QPushButton(self.layoutWidget2)
        self.btn_update.setEnabled(False)
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout_4.addWidget(self.btn_update)
        self.btn_delete = QtWidgets.QPushButton(self.layoutWidget2)
        self.btn_delete.setEnabled(False)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout_4.addWidget(self.btn_delete)
        self.btn_close = QtWidgets.QPushButton(self.layoutWidget2)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_4.addWidget(self.btn_close)

        self.retranslateUi(DialogManageOSC)
        QtCore.QMetaObject.connectSlotsByName(DialogManageOSC)

    def retranslateUi(self, DialogManageOSC):
        _translate = QtCore.QCoreApplication.translate
        DialogManageOSC.setWindowTitle(
            _translate("DialogManageOSC", "Manage OS Charges")
        )
        self.label_print.setText(_translate("DialogManageOSC", "Printing Rate"))
        self.label_stitch.setText(_translate("DialogManageOSC", "Stitching Rate"))
        self.label_4.setText(_translate("DialogManageOSC", "Filter"))
        self.label_5.setText(_translate("DialogManageOSC", "(eg: 3290-BK-G)"))
        self.label_article.setText(_translate("DialogManageOSC", "Article"))
        self.btn_save.setText(_translate("DialogManageOSC", "Save"))
        self.btn_update.setText(_translate("DialogManageOSC", "Update"))
        self.btn_delete.setText(_translate("DialogManageOSC", "Delete"))
        self.btn_close.setText(_translate("DialogManageOSC", "Close"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    DialogManageOSC = QtWidgets.QWidget()
    ui = Ui_DialogManageOSC()
    ui.setupUi(DialogManageOSC)
    DialogManageOSC.show()
    sys.exit(app.exec())
