from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogManageFixedCharge(object):
    def setupUi(self, DialogManageFixedCharge):
        DialogManageFixedCharge.setObjectName("DialogManageFixedCharge")
        DialogManageFixedCharge.resize(310, 206)
        self.widget = QtWidgets.QWidget(DialogManageFixedCharge)
        self.widget.setGeometry(QtCore.QRect(10, 10, 287, 177))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_royality = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_royality.sizePolicy().hasHeightForWidth())
        self.label_royality.setSizePolicy(sizePolicy)
        self.label_royality.setMinimumSize(QtCore.QSize(160, 0))
        self.label_royality.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_royality.setFont(font)
        self.label_royality.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_royality.setObjectName("label_royality")
        self.horizontalLayout.addWidget(self.label_royality)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.text_royality = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_royality.sizePolicy().hasHeightForWidth())
        self.text_royality.setSizePolicy(sizePolicy)
        self.text_royality.setMinimumSize(QtCore.QSize(80, 25))
        self.text_royality.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.text_royality.setFont(font)
        self.text_royality.setObjectName("text_royality")
        self.horizontalLayout.addWidget(self.text_royality)
        self.label_structure_2 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_structure_2.sizePolicy().hasHeightForWidth())
        self.label_structure_2.setSizePolicy(sizePolicy)
        self.label_structure_2.setMinimumSize(QtCore.QSize(15, 0))
        self.label_structure_2.setMaximumSize(QtCore.QSize(15, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_structure_2.setFont(font)
        self.label_structure_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_structure_2.setObjectName("label_structure_2")
        self.horizontalLayout.addWidget(self.label_structure_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_sell_distr = QtWidgets.QLabel(self.widget)
        self.label_sell_distr.setMinimumSize(QtCore.QSize(160, 0))
        self.label_sell_distr.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_sell_distr.setFont(font)
        self.label_sell_distr.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_sell_distr.setObjectName("label_sell_distr")
        self.horizontalLayout_2.addWidget(self.label_sell_distr)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.text_sell_distr = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_sell_distr.sizePolicy().hasHeightForWidth())
        self.text_sell_distr.setSizePolicy(sizePolicy)
        self.text_sell_distr.setMinimumSize(QtCore.QSize(80, 25))
        self.text_sell_distr.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.text_sell_distr.setFont(font)
        self.text_sell_distr.setObjectName("text_sell_distr")
        self.horizontalLayout_2.addWidget(self.text_sell_distr)
        self.label_structure_4 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_structure_4.sizePolicy().hasHeightForWidth())
        self.label_structure_4.setSizePolicy(sizePolicy)
        self.label_structure_4.setMinimumSize(QtCore.QSize(15, 0))
        self.label_structure_4.setMaximumSize(QtCore.QSize(15, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_structure_4.setFont(font)
        self.label_structure_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_structure_4.setObjectName("label_structure_4")
        self.horizontalLayout_2.addWidget(self.label_structure_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_sale_ret = QtWidgets.QLabel(self.widget)
        self.label_sale_ret.setMinimumSize(QtCore.QSize(160, 0))
        self.label_sale_ret.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_sale_ret.setFont(font)
        self.label_sale_ret.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_sale_ret.setObjectName("label_sale_ret")
        self.horizontalLayout_3.addWidget(self.label_sale_ret)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.text_sale_ret = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_sale_ret.sizePolicy().hasHeightForWidth())
        self.text_sale_ret.setSizePolicy(sizePolicy)
        self.text_sale_ret.setMinimumSize(QtCore.QSize(80, 25))
        self.text_sale_ret.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.text_sale_ret.setFont(font)
        self.text_sale_ret.setObjectName("text_sale_ret")
        self.horizontalLayout_3.addWidget(self.text_sale_ret)
        self.label_structure_3 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_structure_3.sizePolicy().hasHeightForWidth())
        self.label_structure_3.setSizePolicy(sizePolicy)
        self.label_structure_3.setMinimumSize(QtCore.QSize(15, 0))
        self.label_structure_3.setMaximumSize(QtCore.QSize(15, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_structure_3.setFont(font)
        self.label_structure_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_structure_3.setObjectName("label_structure_3")
        self.horizontalLayout_3.addWidget(self.label_structure_3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.btn_update = QtWidgets.QPushButton(self.widget)
        self.btn_update.setEnabled(False)
        self.btn_update.setMinimumSize(QtCore.QSize(120, 27))
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout_4.addWidget(self.btn_update)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(DialogManageFixedCharge)
        QtCore.QMetaObject.connectSlotsByName(DialogManageFixedCharge)
        DialogManageFixedCharge.setTabOrder(self.btn_update, self.text_royality)
        DialogManageFixedCharge.setTabOrder(self.text_royality, self.text_sell_distr)
        DialogManageFixedCharge.setTabOrder(self.text_sell_distr, self.text_sale_ret)

    def retranslateUi(self, DialogManageFixedCharge):
        _translate = QtCore.QCoreApplication.translate
        DialogManageFixedCharge.setWindowTitle(_translate("DialogManageFixedCharge", "Manage Fixed Charges"))
        self.label_royality.setText(_translate("DialogManageFixedCharge", "Royality"))
        self.label_structure_2.setText(_translate("DialogManageFixedCharge", "%"))
        self.label_sell_distr.setText(_translate("DialogManageFixedCharge", "Selling and Distribution"))
        self.label_structure_4.setText(_translate("DialogManageFixedCharge", "%"))
        self.label_sale_ret.setText(_translate("DialogManageFixedCharge", "Sales Return"))
        self.label_structure_3.setText(_translate("DialogManageFixedCharge", "%"))
        self.btn_update.setText(_translate("DialogManageFixedCharge", "Update"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogManageFixedCharge = QtWidgets.QWidget()
    ui = Ui_DialogManageFixedCharge()
    ui.setupUi(DialogManageFixedCharge)
    DialogManageFixedCharge.show()
    sys.exit(app.exec())
