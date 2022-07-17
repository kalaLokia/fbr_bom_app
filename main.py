# FIXME: Logging live slow downs GUI
# TODO: Use python logging module
# TODO: Create packaging notes


import sys, os
import datetime
import logging

from PyQt6 import QtWidgets, QtGui

from windows.window_splash_screen import SplashScreen


LOG_FILENAME = './logs.out'
logging.basicConfig(
    filename=LOG_FILENAME, 
    level=logging.DEBUG, 
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def ErrorDialogWindow(title: str, message: str) -> None:
    """Dialog box to display errors"""

    icon = "icons/triangle-exclamation-solid.svg"

    dialog = QtWidgets.QMessageBox()
    dialog.setWindowTitle(title)
    dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
    dialog.setWindowIcon(QtGui.QIcon(icon))
    dialog.setText(message)
    dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    dialog.exec()


if __name__ == "__main__":

    app_ready = False
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        from settings import BASE_DIR, DB_CONN_STR, DB_HOST, DB_NAME

        app_ready = True

    except Exception as e:
        DB_CONN_STR = None
        ErrorDialogWindow(
            "Windows Access Denied",
            "Missing required directory data in application root",
        )

    if DB_CONN_STR == None:
        if app_ready:
            ErrorDialogWindow(
                "[Error 444] Connection Failed!",
                "SQL Server connection parameters not found, failed to launch application.",
            )

    else:
        app.setWindowIcon(QtGui.QIcon(os.path.join(BASE_DIR, "icons", "logo.ico")))

        loader = SplashScreen()
        app_ready = bool(loader.exec())

        # Overcame all possible startup issues, ready to launch the application
        if app_ready:
            from settings import BASE_DIR
            from windows.home_screen import WindowHomeScreen

            try:
                MainWindow = WindowHomeScreen()
                MainWindow.show()
            except:
                logging.exception("App crashed..!!")
            finally:
                sys.exit(app.exec())
