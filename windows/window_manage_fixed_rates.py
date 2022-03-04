from PyQt6 import QtCore, QtGui, QtWidgets

from database.sql_db import query_fetch_fixed_rates, query_update_fixed_rates
from ui.ui_manage_fixed_charges import Ui_DialogManageFixedCharge


class WindowManageFixedCharges(QtWidgets.QWidget):

    close_window = QtCore.pyqtSignal(bool)  # Any changes made to db or not

    def __init__(self) -> None:
        super().__init__()
        self.is_updated: bool = False
        self.ui = Ui_DialogManageFixedCharge()
        self.ui.setupUi(self)
        self.refreshDataModel()
        self.ui.text_royality.textChanged.connect(self.eventValuesChanged)
        self.ui.text_sell_distr.textChanged.connect(self.eventValuesChanged)
        self.ui.text_sale_ret.textChanged.connect(self.eventValuesChanged)
        self.ui.btn_update.clicked.connect(self.buttonUpdate)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_window.emit(self.is_updated)
        return super().closeEvent(a0)

    def refreshDataModel(self):
        fixed_rates = query_fetch_fixed_rates()
        for fc in fixed_rates:
            if fc.rate_type == "RY":
                self.royality = round(fc.value, 2)
                self.ui.text_royality.setText(str(round(fc.value, 2)))
            elif fc.rate_type == "SD":
                self.sell_distr = round(fc.value, 2)
                self.ui.text_sell_distr.setText(str(round(fc.value, 2)))
            elif fc.rate_type == "SR":
                self.sale_ret = round(fc.value, 2)
                self.ui.text_sale_ret.setText(str(round(fc.value, 2)))
        self.is_updated = True
        self.ui.btn_update.setEnabled(False)

    def eventValuesChanged(self, text):
        try:
            ry = float(self.ui.text_royality.text())
            sd = float(self.ui.text_sell_distr.text())
            sr = float(self.ui.text_sale_ret.text())
        except ValueError:
            self.ui.btn_update.setEnabled(False)
            return
        if ry == self.royality and sd == self.sell_distr and sr == self.sale_ret:
            self.ui.btn_update.setEnabled(False)
        else:
            self.ui.btn_update.setEnabled(True)

    def buttonUpdate(self):
        try:
            ry = float(self.ui.text_royality.text())
            sd = float(self.ui.text_sell_distr.text())
            sr = float(self.ui.text_sale_ret.text())
        except ValueError:
            self.eventAlertDialog("Invalid data!", "Only digits are allowed")
            return

        if ry == self.royality:
            ry = None
        if sd == self.sell_distr:
            sd == None
        if sr == self.sale_ret:
            sr == None

        if ry != None or sd != None or sr != None:
            status, res = query_update_fixed_rates(
                royality=ry, sell_distr=sd, sales_ret=sr
            )
            if status:
                self.refreshDataModel()
                self.eventAlertDialog("Successfull", res)
            else:
                self.eventAlertDialog("Failed to Update!", res)

    def eventAlertDialog(self, title, message):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle(title)
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
        dialog.setWindowIcon(QtGui.QIcon("icons/gear-solid.svg"))
        dialog.setText(message)
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        response = dialog.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        return False
