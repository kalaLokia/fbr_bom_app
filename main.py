# TODO: Change the save location to user prefered or ask for location before exporting
# TODO: Progress indicator for bulk exporting
# TODO: Create app log window; detailed logging for all errors, warnings.
# TODO: Create readme
# TODO: Write module level descriptions
# TODO: Create packaging notes


import sys, os

from PyQt6 import QtWidgets, QtGui
from sqlalchemy.exc import InterfaceError, OperationalError, ProgrammingError

from settings import BASE_DIR, DB_CONN_STR, DB_HOST, DB_NAME


def ErrorDialogWindow(title: str, message: str, bug: bool = False) -> None:
    """Dialog box to display errors"""
    icon = "icons/triangle-exclamation-solid.svg"
    if bug:
        icon = "icons/bug-solid.svg"
    dialog = QtWidgets.QMessageBox()
    dialog.setWindowTitle(title)
    dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
    dialog.setWindowIcon(QtGui.QIcon(icon))
    dialog.setText(message)
    dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    dialog.exec()


if __name__ == "__main__":

    ready = False
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setWindowIcon(QtGui.QIcon(os.path.join(BASE_DIR, "icons", "logo.ico")))

    if DB_CONN_STR == None:
        ErrorDialogWindow(
            "[Error 444] Connection Failed!",
            "SQL Server connection parameters not found, failed to lanuch application.",
        )
    else:
        try:
            # Catching exceptions from database.database module
            from windows.home_screen import WindowHomeScreen

            ready = True

        except OperationalError as e:
            if "could not open a connection" in e.args[0].lower():
                ErrorDialogWindow(
                    "[Error 500] Login timeout expired",
                    f'Unable to establish a connection with server "{DB_HOST}". Check if the server is correctly configured and is available to accept connections.',
                )
            else:
                ErrorDialogWindow("[Error 500] Server not found", f"{e.args[0]}", True)
        except InterfaceError as e:
            err = e.args[0].lower()
            if "cannot open database" in err:
                ErrorDialogWindow(
                    "[Error 501] Database Not Accessible",
                    f"Cannot open database {DB_NAME}, check if the database is correctly configured or not.",
                )
            elif "login failed for user" in err:
                ErrorDialogWindow(
                    "[Error 502] Connection Rejected!",
                    "Connection to the server is rejected. Check the username and password configured to access the database.",
                )
            else:
                ErrorDialogWindow(
                    "[Error 503] Connection Rejected", f"{e.args[0]}", True
                )
        except ProgrammingError as e:
            # Unique key constraints with same name already exists !!
            ErrorDialogWindow(
                "[Error 600] Issue with Database",
                "Some tables in your database causing problem. Should only happens if someone created tables manually in db.",
            )
            print(e)
        except Exception as e:
            ErrorDialogWindow("[Error 666] Please report to me!", f"{e.args[0]}", True)
            print(f"Unknown Exception caught\n{e}")

        # All startup issues are cleaned, ready to launch application
        if ready:
            MainWindow = WindowHomeScreen()
            MainWindow.show()
            sys.exit(app.exec())
