import os

from PyQt6 import QtCore, QtGui, QtWidgets

from ui.ui_create_bom import Ui_DialogCreateBom
from core.threads.thread_create_bom import WorkerThreadBom

QtCore.QDir.addSearchPath("icons", "icons")


class WindowCreateBom(QtWidgets.QWidget):

    close_window = QtCore.pyqtSignal(bool)  # Any changes made to db or not

    def __init__(self) -> None:
        super().__init__()
        self.is_updated: bool = False
        self.ui = Ui_DialogCreateBom()
        self.ui.setupUi(self)
        self.ui.progressBar.hide()
        self.ui.btn_choose_bom.clicked.connect(self.chooseBomPath)
        self.ui.btn_choose_materials.clicked.connect(self.chooseMaterialsPath)
        self.ui.btn_update.clicked.connect(self.updateTables)
        self.ui.btn_close.clicked.connect(self.closeDialogWindow)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_window.emit(self.is_updated)
        return super().closeEvent(a0)

    def closeDialogWindow(self):
        self.close_window.emit(self.is_updated)
        # QtCore.QCoreApplication.instance().quit() #quit app

    def chooseBomPath(self) -> None:
        """Opens file dialog for choosing Bom file"""

        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open File", "./data", "Excel Files (*.xlsx)"
        )
        self.ui.text_bom_path.setText(filename[0])

    def chooseMaterialsPath(self):
        """Opens file dialog for choosing Materials file"""

        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open File", "./data", "Excel Files (*.xlsx)"
        )
        self.ui.text_materials_path.setText(filename[0])

    def updateTables(self):
        """Update bom, article list tables."""

        bom_path = self.ui.text_bom_path.text()
        materials_path = self.ui.text_materials_path.text()

        if not os.path.exists(bom_path):
            self.event_show_message(
                False, "Invalid path to file given for bom heirachy."
            )
            return
        if not os.path.exists(materials_path):
            self.event_show_message(False, "Invalid path to file given for materials.")
            return

        # Ask for a confirmation before updating tables entirely
        confirm = self.event_confirm_action()
        if not confirm:
            return

        self.ui.progressBar.setStyleSheet("")
        self.ui.progressBar.show()
        self.ui.progressBar.setValue(1)
        self.worker = WorkerThreadBom(bom_path, materials_path)
        self.worker.start()
        self.worker.update_progress.connect(self.event_progress)
        self.worker.completed.connect(self.event_show_message)

    def event_progress(self, value):
        self.ui.progressBar.setValue(value)

    def event_show_message(self, success, message):
        dialog = QtWidgets.QMessageBox()
        if success:
            dialog.setWindowTitle("Done")
            dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
            self.is_updated = True
        else:
            progress_fail_style = "QProgressBar::chunk{background-color:#db1212;border-radius: 2px;border: 1px solid #a1152a;}QProgressBar{text-align:center;border-radius: 2px;border: 1px solid #a1152a;}"
            self.ui.progressBar.setStyleSheet(progress_fail_style)
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
            "You are going to delete all current bom data from the database, which cannot be restored later.\n\nDo you want to proceed the operation anyway?"
        )
        dialog.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No
        )
        response = dialog.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        return False
