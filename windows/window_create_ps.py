import os
from PyQt6 import QtCore, QtGui, QtWidgets

from core.threads.thread_create_ps import WorkerThreadPriceStructure
from ui.ui_create_price_struct import Ui_DialogUpdateFromFile


class WindowCreatePriceStructure(QtWidgets.QWidget):

    close_window = QtCore.pyqtSignal(bool)  # Any changes made to db or not

    def __init__(self) -> None:
        super().__init__()
        self.is_updated: bool = False
        self.ui = Ui_DialogUpdateFromFile()
        self.ui.setupUi(self)
        self.ui.btn_choose_file.clicked.connect(self.choosePriceStructPath)
        self.ui.btn_close.clicked.connect(self.closeDialogWindow)
        self.ui.btn_update.clicked.connect(self.updateTable)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_window.emit(self.is_updated)
        return super().closeEvent(a0)

    def closeDialogWindow(self):
        self.close_window.emit(self.is_updated)
        # QtCore.QCoreApplication.instance().quit()

    def choosePriceStructPath(self):
        """Opens file dialog for choosing Materials file"""

        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open File", "./data", "Excel Files (*.xlsx)"
        )
        self.ui.text_file_path.setText(filename[0])

    def updateTable(self):

        ps_path = self.ui.text_file_path.text()

        if not os.path.exists(ps_path):
            self.event_show_message(
                False, "Invalid path to file given for Price Structure."
            )
            return

        # Ask for a confirmation before updating tables entirely
        confirm = self.event_confirm_action()
        if not confirm:
            return

        self.worker = WorkerThreadPriceStructure(ps_path)
        self.worker.start()
        self.worker.completed.connect(self.event_show_message)

    def event_show_message(self, success, message):
        dialog = QtWidgets.QMessageBox()
        if success:
            dialog.setWindowTitle("Done")
            dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
            self.is_updated = True
        else:
            dialog.setWindowTitle("Failed!")
            dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)

        dialog.setWindowIcon(QtGui.QIcon("icons/gear-solid.svg"))
        dialog.setText(message)
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        response = dialog.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Ok and success:
            self.closeDialogWindow()

    def event_confirm_action(self):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Confirmation")
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
        dialog.setWindowIcon(QtGui.QIcon("icons/gear-solid.svg"))
        dialog.setText(
            "You are going to delete all current price structure data from the database, which cannot be restored later.\n\nDo you want to proceed the operation anyway?"
        )
        dialog.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No
        )
        response = dialog.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        return False
