from datetime import datetime

from PyQt6 import QtCore, QtGui, QtWidgets

from core.core import LogType
from ui.ui_app_logs import Ui_AppLogs


class WindowAppLogs(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_AppLogs()
        self.ui.setupUi(self)

    def updateLog(self, log_type: LogType, log_msg: str) -> None:

        log = self.ui.text_logs.toHtml()
        now = str(datetime.now().time())
        # color, logtype, text
        fmt = '<p>({}) <font color="{}"><strong>{}:<strong></font> <font color=white> {}</font></p>'
        text = ""
        if log_type == LogType.INFO:
            text = fmt.format(now, "#00ffff", "info", log_msg)
        elif log_type == LogType.WARNING:
            text = fmt.format(now, "#ffff00", "warning", log_msg)
        elif log_type == LogType.ERROR:
            text = fmt.format(now, "#ff0000", "error", log_msg)

        log += text
        # self.ui.text_logs.insertHtml(text)
        self.ui.text_logs.setText(log)
        self.ui.text_logs.moveCursor(QtGui.QTextCursor.MoveOperation.End)

    # Temperory func till freeze issue is resolved
    def updateLogBulk(self, new_log):
        log = self.ui.text_logs.toHtml()
        log += new_log
        self.ui.text_logs.setText(log)
        self.ui.text_logs.moveCursor(QtGui.QTextCursor.MoveOperation.End)
