from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6.QtGui import QMovie, QIcon
from sqlalchemy.exc import InterfaceError, OperationalError, ProgrammingError


class WorkerThreadInitialize(QtCore.QThread):
    """
    Error checks while initializing application.
    """

    completed = QtCore.pyqtSignal(bool, str, str)

    def __init__(self) -> None:
        super(QtCore.QThread, self).__init__()

        self.ready = False

    def run(self):
        """Try for the imports and sql connection"""

        try:
            from settings import BASE_DIR, DB_CONN_STR, DB_HOST, DB_NAME
        except Exception as e:
            DB_CONN_STR = None
            self.completed.emit(
                self.ready, "Windows Access Denied", "Missing required directory data!"
            )
            return

        if DB_CONN_STR == None:
            self.completed.emit(
                self.ready,
                "[Error 444] Connection Failed!",
                "SQL Server connection parameters not found, failed to lanuch application.",
            )
        else:
            try:
                from database import database

                self.ready = True
                self.completed.emit(self.ready, "", "")

            except OperationalError as e:
                if "could not open a connection" in e.args[0].lower():
                    self.completed.emit(
                        self.ready,
                        "[Error 500] Login timeout expired",
                        f'Unable to establish a connection with server "{DB_HOST}". Check if the server is correctly configured and is available to accept connections.',
                    )
                else:
                    self.completed.emit(
                        self.ready, "[Error 500] Server not found", f"{e.args[0]}"
                    )
            except InterfaceError as e:
                err = e.args[0].lower()
                if "cannot open database" in err:
                    self.completed.emit(
                        self.ready,
                        "[Error 501] Database Not Accessible",
                        f"Cannot open database {DB_NAME}, check if the database is correctly configured or not.",
                    )
                elif "login failed for user" in err:
                    self.completed.emit(
                        self.ready,
                        "[Error 502] Connection Rejected!",
                        "Connection to the server is rejected. Check the username and password configured to access the database.",
                    )
                elif "no default driver specified" in err:
                    self.completed.emit(
                        self.ready,
                        "[Error 504] ODBC Driver Missing!",
                        'Driver "ODBC Driver 17 for SQL Server" is missing in your system, connection request failed!',
                    )
                else:
                    self.completed.emit(
                        self.ready,
                        "[Error 600] Connection Failed",
                        f"{e.args[0]}",
                    )
            except ProgrammingError as e:
                # Unique key constraints with same name already exists !!
                self.completed.emit(
                    self.ready,
                    "[Error 401] Issue with Database",
                    "Some tables in your database causing problem. Should only happens if someone created tables manually in db.",
                )
            except Exception as e:
                self.completed.emit(
                    self.ready, "[Error 666] Please report to me!", f"{e.args[0]}"
                )


class SplashScreen(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(800, 600)
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.ready = False
        self.label_animation = QtWidgets.QLabel(self)
        self.movie = QMovie("./icons/loader.gif")
        self.label_animation.setMovie(self.movie)

        self.worker = WorkerThreadInitialize()
        self.worker.start()
        self.worker.completed.connect(self.handleInitialization)

        self.movie.start()

        self.show()

    # def startAnimation(self):
    #     self.movie.start()

    # def stopAnimation(self):
    #     self.movie.stop()
    #     self.close()

    def stopInitializingApp(self):
        """Stop animation and return False to quit MainWindow"""
        self.movie.stop()
        self.done(0)

    def startInitializingApp(self):
        """Stop animation and return True to start MainWindow"""
        self.movie.stop()
        self.done(1)

    def handleInitialization(self, ready: bool, err_title: str, err_desc: str):
        self.ready = ready
        if not ready:
            icon = "icons/triangle-exclamation-solid.svg"
            if err_title.startswith("[Error 6"):
                icon = "icons/bug-solid.svg"
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle(err_title)
            dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dialog.setWindowIcon(QIcon(icon))
            dialog.setText(err_desc)
            dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            self.stopInitializingApp()
            dialog.exec()
        else:
            self.startInitializingApp()
