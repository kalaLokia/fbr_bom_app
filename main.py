# FIXME: Logging live slow downs GUI
# TODO: Use python logging module
# TODO: Create readme
# TODO: Write module level descriptions
# TODO: Create packaging notes


import sys, os

from PyQt6 import QtWidgets, QtGui

from windows.window_splash_screen import SplashScreen


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

            # Can include a `try-catch` to setup up an app fail logging
            MainWindow = WindowHomeScreen()
            MainWindow.show()
            sys.exit(app.exec())
