from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from database.database import PriceStructure
from database.sql_db import (
    query_add_pstructure,
    query_delete_pstructure,
    query_fetch_all_price_structure,
    query_update_pstructure,
)
from ui.ui_manage_ps import Ui_DialogManagePS

QtCore.QDir.addSearchPath("icons", "icons")


class WindowManagePriceStructure(QtWidgets.QWidget):

    close_window = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_DialogManagePS()
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
        self.ui.text_mrp.textChanged.connect(self.eventMrpChanged)
        self.ui.tv_filter_box.selectionModel().selectionChanged.connect(
            self.eventTableSelectionChanged
        )
        self.ui.combo_structure.currentTextChanged.connect(self.eventComboChanged)
        self.ui.btn_close.clicked.connect(self.closeDialogWindow)
        self.ui.btn_save.clicked.connect(self.saveNewRecord)
        self.ui.btn_update.clicked.connect(self.updateRecord)
        self.ui.btn_delete.clicked.connect(self.deleteRecord)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_window.emit()
        return super().closeEvent(a0)

    def refreshDataModel(self):
        self.pstructures = query_fetch_all_price_structure()
        self.ps_uniques = {}
        self.model = QtGui.QStandardItemModel(len(self.pstructures), 2)
        self.model.setHorizontalHeaderLabels(["Price Structure", "Basic Rate"])
        for row, ps in enumerate(self.pstructures):
            self.ps_uniques[ps.unique_code] = ps
            pstructure = QtGui.QStandardItem(ps.unique_code)
            basic = QtGui.QStandardItem(str(ps.basic))
            basic.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.model.setItem(row, 0, pstructure)
            self.model.setItem(row, 1, basic)

        self.filter_proxy_model.setSourceModel(self.model)

    def closeDialogWindow(self):
        self.close_window.emit()

    def eventMrpChanged(self, text):
        mrp = 0.0
        try:
            mrp = float(text)
        except ValueError:
            pass

        key = "{}-{}".format(self.ui.combo_structure.currentText(), text)
        if key in self.ps_uniques.keys():
            self.ui.btn_save.setEnabled(False)
            self.ui.btn_update.setEnabled(True)
        else:
            self.ui.btn_update.setEnabled(False)
            self.ui.btn_save.setEnabled(True)

    def eventComboChanged(self, value):
        key = "{}-{}".format(value, self.ui.text_mrp.text())
        if key in self.ps_uniques.keys():
            self.ui.btn_save.setEnabled(False)
            self.ui.btn_update.setEnabled(True)
        else:
            self.ui.btn_update.setEnabled(False)
            self.ui.btn_save.setEnabled(True)

    def eventTableSingleClicked(self, modelIndex: QtCore.QModelIndex):
        self.clearTextBoxValues()

    def eventTableDoubleClicked(self, modelIndex: QtCore.QModelIndex):
        key = self.model.index(modelIndex.row(), 0).data()

        self.ui.text_mrp.setText(str(self.ps_uniques[key].mrp))
        self.ui.text_basic.setText(str(self.ps_uniques[key].basic))
        self.ui.combo_structure.setCurrentText(self.ps_uniques[key].get_price_struct)

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
        self.ui.text_mrp.setText("")
        self.ui.text_basic.setText("")
        self.ui.btn_update.setEnabled(False)
        self.ui.btn_save.setEnabled(False)

    def updateRecord(self):
        """Update existing record in the database"""
        # Button active only if it is existing in loaded models
        ps = PriceStructure()
        ps.to_ps_code(self.ui.combo_structure.currentText())
        try:
            # mrp actually not changes
            ps.mrp = float(self.ui.text_mrp.text())
            ps.basic = float(self.ui.text_basic.text())
        except ValueError:
            self.eventAlertDialog("Invalid data!", "Only digits are allowed!")
            return

        if ps.mrp <= 0 or ps.basic <= 0:
            self.eventAlertDialog(
                "Invalid data!", "Rates cannot be zero or less, check your input."
            )
            return

        confirm = self.eventConfirmationDialog(
            f"You are going to update values for {ps.unique_code}.\n\nDo you want to proceed ?"
        )
        if confirm:
            status, res = query_update_pstructure(ps)
            if status:
                self.refreshDataModel()
                self.clearTextBoxValues()
                self.eventAlertDialog("Updated", res)
            else:
                self.eventAlertDialog("Failed to Update!", res)

    def saveNewRecord(self):
        """Save new record in the database"""

        ps = PriceStructure()
        ps.to_ps_code(self.ui.combo_structure.currentText())

        try:
            ps.mrp = float(self.ui.text_mrp.text())
            ps.basic = float(self.ui.text_basic.text())
        except ValueError:
            self.eventAlertDialog("Invalid data!", "Only digits are allowed!")
            return

        if ps.mrp <= 0 or ps.basic <= 0:
            self.eventAlertDialog(
                "Invalid data!", "Rates cannot be zero or less, check your input."
            )
            return

        confirm = self.eventConfirmationDialog(
            f"You are going to add new Price Structure {ps.unique_code}.\n\nDo you want to proceed ?"
        )
        if confirm:
            status, res = query_add_pstructure(ps)
            if status:
                self.refreshDataModel()
                self.clearTextBoxValues()
                self.eventAlertDialog("Successful", res)
            else:
                self.eventAlertDialog("Failed to Add!", res)

    def deleteRecord(self):
        """Delete existing record in the database"""

        selections = self.ui.tv_filter_box.selectedIndexes()
        pss = list(
            set(
                self.ps_uniques[self.model.index(selection.row(), 0).data()]
                for selection in selections
            )
        )
        if len(pss) > 1:
            confirm = False
            self.eventAlertDialog(
                "Sorry, little Confused!",
                "Please select only one item, I cannot delete multiple price structures together.",
            )
            return
        else:
            confirm = self.eventConfirmationDialog(
                f"You are going to remove {pss[-1].unique_code} from database.\n\nDo you want to proceed?"
            )

        if confirm:
            ps = pss[-1]
            status, res = query_delete_pstructure(ps)
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
