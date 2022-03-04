from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


from ui.ui_manage_osc import Ui_DialogManageOSC
from database.sql_db import (
    query_fetch_all_os_charges,
    query_add_os_charge,
    query_update_os_charge,
    query_delete_os_charges,
)
from database.database import OSCharges

QtCore.QDir.addSearchPath("icons", "icons")


class WindowManageOsCharges(QtWidgets.QWidget):

    close_window = QtCore.pyqtSignal(bool)  # Any changes made to db or not

    def __init__(self) -> None:
        super().__init__()
        self.is_updated: bool = False
        self.ui = Ui_DialogManageOSC()
        self.ui.setupUi(self)
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.refreshDataModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.filter_proxy_model.setFilterKeyColumn(0)

        self.ui.text_filter.textChanged.connect(
            self.filter_proxy_model.setFilterRegularExpression
        )
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
        self.ui.tv_filter_box.clicked.connect(self.eventTableSingleClicked)
        self.ui.tv_filter_box.doubleClicked.connect(self.eventTableDoubleClicked)
        self.ui.text_article.textChanged.connect(self.eventArticleChanged)
        self.ui.tv_filter_box.selectionModel().selectionChanged.connect(
            self.eventTableSelectionChanged
        )
        self.ui.btn_close.clicked.connect(self.closeDialogWindow)
        self.ui.btn_save.clicked.connect(self.saveNewRecord)
        self.ui.btn_update.clicked.connect(self.updateRecord)
        self.ui.btn_delete.clicked.connect(self.deleteRecord)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_window.emit(self.is_updated)
        return super().closeEvent(a0)

    def closeDialogWindow(self):
        self.close_window.emit(self.is_updated)
        # QtCore.QCoreApplication.instance().quit()

    def refreshDataModel(self):
        self.os_charges = query_fetch_all_os_charges()
        self.articles = [e.article for e in self.os_charges]
        self.model = QtGui.QStandardItemModel(len(self.os_charges), 3)
        self.model.setHorizontalHeaderLabels(["Article", "Printing", "Stitching"])
        for row, osc in enumerate(self.os_charges):
            article = QtGui.QStandardItem(osc.article)
            print_rate = QtGui.QStandardItem(str(osc.printing))
            stitch_rate = QtGui.QStandardItem(str(osc.stitching))
            print_rate.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            stitch_rate.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.model.setItem(row, 0, article)
            self.model.setItem(row, 1, print_rate)
            self.model.setItem(row, 2, stitch_rate)
        self.is_updated = True
        self.filter_proxy_model.setSourceModel(self.model)

    def eventArticleChanged(self, text):
        if text.strip().upper() in self.articles:
            self.ui.btn_save.setEnabled(False)
            self.ui.btn_update.setEnabled(True)
        else:
            self.ui.btn_update.setEnabled(False)
            self.ui.btn_save.setEnabled(True)

    def eventTableSingleClicked(self, modelIndex: QtCore.QModelIndex):
        self.clearTextBoxValues()

    def eventTableDoubleClicked(self, modelIndex: QtCore.QModelIndex):
        row = modelIndex.row()
        self.ui.text_article.setText(self.os_charges[row].article)
        self.ui.text_print_rate.setText(str(self.os_charges[row].printing))
        self.ui.text_stitch_rate.setText(str(self.os_charges[row].stitching))

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

    def clearTextBoxValues(self):
        """Clear all values in text boxes and disable buttons"""
        self.ui.text_article.setText("")
        self.ui.text_print_rate.setText("")
        self.ui.text_stitch_rate.setText("")
        self.ui.btn_update.setEnabled(False)
        self.ui.btn_save.setEnabled(False)

    def updateRecord(self):
        """Update existing record in the database"""
        # Button active only if it is existing in loaded models
        osc = OSCharges()
        osc.article = self.ui.text_article.text().strip().upper()
        try:
            osc.print_rate = float(self.ui.text_print_rate.text())
            osc.stitch_rate = float(self.ui.text_stitch_rate.text())
        except ValueError:
            self.eventAlertDialog("Invalid data!", "Only digits are allowed!")
            return

        if osc.print_rate < 0 or osc.stitch_rate < 0:
            self.eventAlertDialog(
                "Invalid data!", "Rates cannot be lesser than 0, check your input."
            )
            return

        confirm = self.eventConfirmationDialog(
            f"You are going to update values for {osc.article}.\n\nDo you want to proceed ?"
        )
        if confirm:
            status, res = query_update_os_charge(osc)
            if status:
                self.refreshDataModel()
                self.clearTextBoxValues()
                self.eventAlertDialog("Updated", res)
            else:
                self.eventAlertDialog("Failed to Update!", res)

    def saveNewRecord(self):
        """Save new record in the database"""
        osc = OSCharges()
        osc.article = self.ui.text_article.text().strip().upper()
        try:
            osc.print_rate = float(self.ui.text_print_rate.text())
            osc.stitch_rate = float(self.ui.text_stitch_rate.text())
        except:
            self.eventAlertDialog("Invalid data!", "Only digits are allowed!")
            return

        if osc.print_rate < 0 or osc.stitch_rate < 0:
            self.eventAlertDialog(
                "Invalid data!", "Rates cannot be lesser than 0, check your input."
            )
            return

        confirm = self.eventConfirmationDialog(
            f"You are going to add new Os Charge for {osc.article}.\n\nDo you want to proceed ?"
        )
        if confirm:
            status, res = query_add_os_charge(osc)
            if status:
                self.refreshDataModel()
                self.clearTextBoxValues()
                self.eventAlertDialog("Successful", res)
            else:
                self.eventAlertDialog("Failed to Add!", res)

    def deleteRecord(self):
        """Delete existing record in the database"""
        selections = self.ui.tv_filter_box.selectedIndexes()
        rows = list(set(selection.row() for selection in selections))
        if len(rows) > 1:
            confirm = self.eventConfirmationDialog(
                f"You are going to remove {len(rows)} records from the database, this cannot be undone later.\n\nDo you want to proceed anyway?"
            )
        else:
            confirm = self.eventConfirmationDialog(
                f"You are going to remove {self.os_charges[rows[-1]].article} from database, this cannot be reverted back later.\n\nDo you want to proceed?"
            )

        if confirm:
            list_items = [self.os_charges[row].article for row in rows]
            status, res = query_delete_os_charges(list_items)
            if status:
                self.refreshDataModel()
                self.clearTextBoxValues()
                self.eventAlertDialog("Successful", res)
            else:
                self.eventAlertDialog("Failed to delete!", res)

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
