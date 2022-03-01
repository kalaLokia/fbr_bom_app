from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from database.database import FixedRates
from database.sql_db import (
    query_add_expense,
    query_delete_expenses,
    query_fetch_expenses,
    query_update_expenses,
)
from ui.ui_manage_expenses import Ui_DialogManageExpenses


class WindowManageExpenses(QtWidgets.QWidget):

    close_window = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_DialogManageExpenses()
        self.ui.setupUi(self)
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.refreshDataModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.ui.tv_filter_box.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.ui.tv_filter_box.setEditTriggers(
            QtWidgets.QTableView.EditTrigger.NoEditTriggers
        )
        self.ui.tv_filter_box.setModel(self.filter_proxy_model)
        self.ui.tv_filter_box.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.ui.text_filter.textChanged.connect(
            self.filter_proxy_model.setFilterRegularExpression
        )
        self.ui.tv_filter_box.clicked.connect(self.eventTableSingleClicked)
        self.ui.tv_filter_box.doubleClicked.connect(self.eventTableDoubleClicked)
        self.ui.tv_filter_box.selectionModel().selectionChanged.connect(
            self.eventTableSelectionChanged
        )
        self.ui.text_name.textChanged.connect(self.eventExpenseNameChanged)
        self.ui.btn_close.clicked.connect(self.buttonCloseDialogWindow)
        self.ui.btn_add_new.clicked.connect(self.buttonAddNew)
        self.ui.btn_update.clicked.connect(self.buttonUpdate)
        self.ui.btn_delete.clicked.connect(self.buttonDelete)

    def refreshDataModel(self):
        self.expenses = query_fetch_expenses()
        self.list_expenses = [e.name.lower() for e in self.expenses]
        self.model = QtGui.QStandardItemModel(len(self.expenses), 2)
        self.model.setHorizontalHeaderLabels(["Expenses or Overheads", "Rate"])
        for row, exp in enumerate(self.expenses):
            exp_name = QtGui.QStandardItem(exp.name)
            exp_rate = QtGui.QStandardItem(str(round(exp.value, 2)))
            self.model.setItem(row, 0, exp_name)
            self.model.setItem(row, 1, exp_rate)
        self.filter_proxy_model.setSourceModel(self.model)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_window.emit()
        return super().closeEvent(a0)

    def eventExpenseNameChanged(self, text: str):
        if text.strip().lower() in self.list_expenses:
            self.ui.btn_add_new.setEnabled(False)
            self.ui.btn_update.setEnabled(True)
        else:
            self.ui.btn_update.setEnabled(False)
            self.ui.btn_add_new.setEnabled(True)

    def eventTableSingleClicked(self, modelIndex: QtCore.QModelIndex):
        self.clearTextBoxValues()

    def eventTableDoubleClicked(self, modelIndex: QtCore.QModelIndex):
        self.ui.text_name.setText(self.expenses[modelIndex.row()].name)
        self.ui.text_rate.setText(str(round(self.expenses[modelIndex.row()].value, 2)))

    def eventTableSelectionChanged(
        self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection
    ):
        selections = self.ui.tv_filter_box.selectedIndexes()
        count = len(set(selection.row() for selection in selections))

        if count > 1:
            self.clearTextBoxValues()
            self.ui.btn_delete.setEnabled(True)
        elif count == 1:
            self.ui.btn_delete.setEnabled(True)
        else:
            self.ui.btn_delete.setEnabled(False)

    def buttonCloseDialogWindow(self):
        self.close_window.emit()

    def buttonAddNew(self):
        """Add new expeneses or overhead in the database"""

        text = self.ui.text_name.text().strip()
        if text == "":
            return
        rate = 0
        try:
            rate = float(self.ui.text_rate.text().strip())
        except ValueError:
            self.eventAlertDialog("Invalid data!", "Only digits are allowed for rates")
            return

        exp = FixedRates()
        exp.name = text
        exp.value = rate
        exp.rate_type = "OH"
        exp.value_fmt = "INR"

        confirm = self.eventConfirmationDialog(
            "Are you sure, you want to add new expenses?"
        )
        if confirm:
            status, res = query_add_expense(exp)
            if status:
                self.refreshDataModel()
                self.clearTextBoxValues()
                self.eventAlertDialog("Successfull", res)
            else:
                self.eventAlertDialog("Failed to Add!", res)

    def buttonUpdate(self):
        """Update the rate of a existing record"""
        text = self.ui.text_name.text().strip()
        rate = 0
        try:
            rate = float(self.ui.text_rate.text().strip())
        except ValueError:
            self.eventAlertDialog("Invalid data!", "Only digits are allowed for rates")
            return
        confirm = self.eventConfirmationDialog(
            f"Are you sure, you want to update {text}?"
        )
        if confirm:
            status, res = query_update_expenses(text, rate)
            if status:
                self.refreshDataModel()
                self.clearTextBoxValues()
                self.eventAlertDialog("Successfull", res)
            else:
                self.eventAlertDialog("Failed to Update!", res)

    def buttonDelete(self):
        """Deletes the selected items from the database permanently"""

        selections = self.ui.tv_filter_box.selectedIndexes()
        rows = list(set(selection.row() for selection in selections))
        if len(rows) > 0:
            confirm = self.eventConfirmationDialog(
                "Are you sure to remove the selected expenses/overheads ?"
            )

            if confirm:
                list_items = [self.expenses[row].name for row in rows]
                status, res = query_delete_expenses(list_items)
                if status:
                    self.refreshDataModel()
                    self.clearTextBoxValues()
                    self.eventAlertDialog("Successfull", res)
                else:
                    self.eventAlertDialog("Failed to delete!", res)

    def clearTextBoxValues(self):
        self.ui.text_name.setText("")
        self.ui.text_rate.setText("")
        self.ui.btn_update.setEnabled(False)
        self.ui.btn_add_new.setEnabled(False)

    def eventConfirmationDialog(self, message):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Confirmation")
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
        dialog.setWindowIcon(QtGui.QIcon("icons/gear-solid.svg"))
        dialog.setText(message)
        dialog.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No
        )
        response = dialog.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        return False

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
