from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from pandas import DataFrame

from core.utils.calculate_bom import BillOfMaterial
from core.utils.cost_analysis import calculateProfit, generate_bulk_report
from core.utils.create_excel_report import ExcelReporting
from database import sql_db
from database.sql_db import PriceStructure, OSCharges, Article
from windows.window_create_bom import WindowCreateBom
from windows.window_create_osc import WindowCreateOsCharges
from windows.window_create_ps import WindowCreatePriceStructure


class Ui_MainWindow(object):
    """Main Window of the app"""

    def __init__(self) -> None:
        super().__init__()
        self.menu_items = {}
        articles = sql_db.query_list_articles_all()
        self.fixed_rates = sql_db.query_fetch_fixed_rates()
        self.model = QtGui.QStandardItemModel(len(articles), 1)
        self.model.setHorizontalHeaderLabels(["Articles"])
        self.articles_dict: dict[str, tuple[Article, PriceStructure, OSCharges]] = {}
        for row, article in enumerate(articles):
            if article[0].mrp != 0:
                key = f"{article[0].article}  - ₹{article[0].mrp}"
            else:
                key = f"{article[0].article}  - ###"
            item = QtGui.QStandardItem(key)
            self.articles_dict[key] = article
            item.setFlags(
                Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable
            )
            item.setCheckState(Qt.CheckState.Unchecked)
            self.model.setItem(row, 0, item)
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive
        )
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.is_all_selected = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(879, 638)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("icons/favicon.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(
            "QWidget{ background-color:rgb(202, 234, 255) }\n"
            "\n"
            "QMenuBar::item:selected{ background: rgb(235, 248, 255) }\n"
            "\n"
            "QMenu::item:selected {  background:rgb(65, 163, 255) }\n"
            "\n"
            "QLabel{background-color:transparent;border:0px}\n"
            "\n"
            ""
        )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(
            "QPushButton::pressed {  background:rgb(144, 198, 255) }\n" ""
        )
        self.centralwidget.setObjectName("centralwidget")
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setGeometry(QtCore.QRect(3, 1, 871, 595))
        self.main_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.main_frame.setObjectName("main_frame")
        self.main_left_frame = QtWidgets.QFrame(self.main_frame)
        self.main_left_frame.setGeometry(QtCore.QRect(8, 8, 310, 580))
        self.main_left_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.main_left_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.main_left_frame.setObjectName("main_left_frame")
        self.layoutWidget = QtWidgets.QWidget(self.main_left_frame)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 27, 296, 535))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMaximumSize
        )
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(
            2,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 0, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(280, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.lineEdit.setObjectName("lineEdit")
        # Connecting data with filter search area
        self.lineEdit.textChanged.connect(
            self.filter_proxy_model.setFilterRegularExpression
        )
        self.verticalLayout.addWidget(self.lineEdit)
        self.tableView = QtWidgets.QTableView(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setMinimumSize(QtCore.QSize(280, 300))
        self.tableView.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.tableView.setObjectName("tableView")
        # TableView extra functionality #List to display
        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.tableView.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self.tableView.setModel(self.filter_proxy_model)
        self.tableView.doubleClicked.connect(self.tableDoubleClicked)
        self.tableView.clicked.connect(self.tableSingleClicked)
        self.tableView.selectionModel().selectionChanged.connect(
            self.tableSelectionChanged
        )
        self.tableView.findChild(QtWidgets.QAbstractButton).clicked.connect(
            self.tableSelectAll
        )
        self.verticalLayout.addWidget(self.tableView)
        spacerItem1 = QtWidgets.QSpacerItem(
            20,
            30,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            20,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_2.addItem(spacerItem2)
        self.button_show_stats = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.button_show_stats.sizePolicy().hasHeightForWidth()
        )
        self.button_show_stats.setSizePolicy(sizePolicy)
        self.button_show_stats.setMinimumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.button_show_stats.setFont(font)
        self.button_show_stats.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.button_show_stats.setObjectName("button_show_stats")

        self.horizontalLayout_2.addWidget(self.button_show_stats)
        spacerItem3 = QtWidgets.QSpacerItem(
            20,
            20,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(
            20,
            13,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_export_xl = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.button_export_xl.sizePolicy().hasHeightForWidth()
        )
        self.button_export_xl.setSizePolicy(sizePolicy)
        self.button_export_xl.setMinimumSize(QtCore.QSize(90, 40))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.button_export_xl.setFont(font)
        self.button_export_xl.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.button_export_xl.setObjectName("button_export_xl")
        self.horizontalLayout.addWidget(self.button_export_xl)
        spacerItem5 = QtWidgets.QSpacerItem(
            50,
            30,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem5)
        self.button_export_summary = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.button_export_summary.sizePolicy().hasHeightForWidth()
        )
        self.button_export_summary.setSizePolicy(sizePolicy)
        self.button_export_summary.setMinimumSize(QtCore.QSize(90, 40))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.button_export_summary.setFont(font)
        self.button_export_summary.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.button_export_summary.setObjectName("button_export_summary")
        self.horizontalLayout.addWidget(self.button_export_summary)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem6 = QtWidgets.QSpacerItem(
            2,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_3.addItem(spacerItem6)
        self.label = QtWidgets.QLabel(self.main_frame)
        self.label.setGeometry(QtCore.QRect(430, 40, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Rockwell Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.main_frame)
        self.line.setGeometry(QtCore.QRect(430, 70, 331, 20))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.button_export_xl_sub = QtWidgets.QPushButton(self.main_frame)
        self.button_export_xl_sub.setGeometry(QtCore.QRect(820, 10, 41, 31))
        self.button_export_xl_sub.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap("icons/file-export-solid.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.button_export_xl_sub.setIcon(icon1)
        self.button_export_xl_sub.setObjectName("button_export_xl_sub")
        self.layoutWidget1 = QtWidgets.QWidget(self.main_frame)
        self.layoutWidget1.setGeometry(QtCore.QRect(330, 100, 531, 301))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_2 = QtWidgets.QWidget(self.layoutWidget1)
        self.widget_2.setMaximumSize(QtCore.QSize(122, 63))
        self.widget_2.setStyleSheet(
            "background-color:rgb(255, 255, 255);\n"
            "border:1px solid black;\n"
            "border-radius:20px;"
        )
        self.widget_2.setObjectName("widget_2")
        self.label_stich = QtWidgets.QLabel(self.widget_2)
        self.label_stich.setEnabled(True)
        self.label_stich.setGeometry(QtCore.QRect(10, 10, 100, 20))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_stich.sizePolicy().hasHeightForWidth())
        self.label_stich.setSizePolicy(sizePolicy)
        self.label_stich.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Emoji")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_stich.setFont(font)
        self.label_stich.setAutoFillBackground(False)
        self.label_stich.setStyleSheet("border:0px solid transperant;")
        self.label_stich.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_stich.setObjectName("label_stich")
        self.label_Vstitch = QtWidgets.QLabel(self.widget_2)
        self.label_Vstitch.setGeometry(QtCore.QRect(10, 30, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_Vstitch.setFont(font)
        self.label_Vstitch.setStyleSheet("border:0px;")
        self.label_Vstitch.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_Vstitch.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vstitch.setObjectName("label_Vstitch")
        self.horizontalLayout_4.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.layoutWidget1)
        self.widget_3.setMaximumSize(QtCore.QSize(122, 65))
        self.widget_3.setStyleSheet(
            "background-color:rgb(255, 255, 255);\n"
            "border:1px solid black;\n"
            "border-radius:20px;"
        )
        self.widget_3.setObjectName("widget_3")
        self.label_print = QtWidgets.QLabel(self.widget_3)
        self.label_print.setEnabled(True)
        self.label_print.setGeometry(QtCore.QRect(10, 10, 100, 20))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_print.sizePolicy().hasHeightForWidth())
        self.label_print.setSizePolicy(sizePolicy)
        self.label_print.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Emoji")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_print.setFont(font)
        self.label_print.setAutoFillBackground(False)
        self.label_print.setStyleSheet("border:0px;")
        self.label_print.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_print.setObjectName("label_print")
        self.label_Vprint = QtWidgets.QLabel(self.widget_3)
        self.label_Vprint.setGeometry(QtCore.QRect(10, 30, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_Vprint.setFont(font)
        self.label_Vprint.setStyleSheet("border:0px;")
        self.label_Vprint.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_Vprint.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vprint.setObjectName("label_Vprint")
        self.horizontalLayout_4.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.layoutWidget1)
        self.widget_4.setMaximumSize(QtCore.QSize(122, 65))
        self.widget_4.setStyleSheet(
            "background-color:rgb(255, 255, 255);\n"
            "border:1px solid black;\n"
            "border-radius:20px;"
        )
        self.widget_4.setObjectName("widget_4")
        self.label_mc = QtWidgets.QLabel(self.widget_4)
        self.label_mc.setEnabled(True)
        self.label_mc.setGeometry(QtCore.QRect(10, 10, 100, 20))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_mc.sizePolicy().hasHeightForWidth())
        self.label_mc.setSizePolicy(sizePolicy)
        self.label_mc.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Emoji")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_mc.setFont(font)
        self.label_mc.setAutoFillBackground(False)
        self.label_mc.setStyleSheet("border:0px;")
        self.label_mc.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_mc.setObjectName("label_mc")
        self.label_Vmc = QtWidgets.QLabel(self.widget_4)
        self.label_Vmc.setGeometry(QtCore.QRect(10, 30, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_Vmc.setFont(font)
        self.label_Vmc.setStyleSheet("border:0px;")
        self.label_Vmc.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_Vmc.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vmc.setObjectName("label_Vmc")
        self.horizontalLayout_4.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self.layoutWidget1)
        self.widget_5.setMaximumSize(QtCore.QSize(122, 65))
        self.widget_5.setStyleSheet(
            "background-color:rgb(255, 255, 255);\n"
            "border:1px solid black;\n"
            "border-radius:20px;"
        )
        self.widget_5.setObjectName("widget_5")
        self.label_cop = QtWidgets.QLabel(self.widget_5)
        self.label_cop.setEnabled(True)
        self.label_cop.setGeometry(QtCore.QRect(10, 10, 100, 20))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_cop.sizePolicy().hasHeightForWidth())
        self.label_cop.setSizePolicy(sizePolicy)
        self.label_cop.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Emoji")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_cop.setFont(font)
        self.label_cop.setAutoFillBackground(False)
        self.label_cop.setStyleSheet("border:0px;")
        self.label_cop.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_cop.setObjectName("label_cop")
        self.label_Vcop = QtWidgets.QLabel(self.widget_5)
        self.label_Vcop.setGeometry(QtCore.QRect(10, 30, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_Vcop.setFont(font)
        self.label_Vcop.setStyleSheet("border:0px;")
        self.label_Vcop.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_Vcop.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vcop.setObjectName("label_Vcop")
        self.horizontalLayout_4.addWidget(self.widget_5)
        self.verticalLayout_12.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget_6 = QtWidgets.QWidget(self.layoutWidget1)
        self.widget_6.setMinimumSize(QtCore.QSize(120, 0))
        self.widget_6.setMaximumSize(QtCore.QSize(122, 65))
        self.widget_6.setStyleSheet(
            "background-color:rgb(255, 255, 255);\n"
            "border:1px solid black;\n"
            "border-radius:20px;"
        )
        self.widget_6.setObjectName("widget_6")
        self.label_Vbasic = QtWidgets.QLabel(self.widget_6)
        self.label_Vbasic.setGeometry(QtCore.QRect(10, 30, 100, 20))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_Vbasic.setFont(font)
        self.label_Vbasic.setStyleSheet("border:0px;")
        self.label_Vbasic.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_Vbasic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vbasic.setObjectName("label_Vbasic")
        self.label_basic = QtWidgets.QLabel(self.widget_6)
        self.label_basic.setEnabled(True)
        self.label_basic.setGeometry(QtCore.QRect(10, 10, 100, 15))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_basic.sizePolicy().hasHeightForWidth())
        self.label_basic.setSizePolicy(sizePolicy)
        self.label_basic.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Emoji")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_basic.setFont(font)
        self.label_basic.setAutoFillBackground(False)
        self.label_basic.setStyleSheet("border:0px;")
        self.label_basic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_basic.setObjectName("label_basic")
        self.horizontalLayout_5.addWidget(self.widget_6)
        self.widget = QtWidgets.QWidget(self.layoutWidget1)
        self.widget.setMinimumSize(QtCore.QSize(120, 120))
        self.widget.setMaximumSize(QtCore.QSize(160, 140))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.widget.setFont(font)
        self.widget.setStyleSheet(
            "background-color:rgb(255, 255, 255);\n"
            "border:1px solid black;\n"
            "border-radius:60px;"
        )
        self.widget.setObjectName("widget")
        self.label_netm = QtWidgets.QLabel(self.widget)
        self.label_netm.setEnabled(True)
        self.label_netm.setGeometry(QtCore.QRect(30, 10, 100, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_netm.sizePolicy().hasHeightForWidth())
        self.label_netm.setSizePolicy(sizePolicy)
        self.label_netm.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Emoji")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_netm.setFont(font)
        self.label_netm.setAutoFillBackground(False)
        self.label_netm.setStyleSheet("border:0px;\n" "background-color:transparent;")
        self.label_netm.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_netm.setObjectName("label_netm")
        self.label_Vnetm = QtWidgets.QLabel(self.widget)
        self.label_Vnetm.setGeometry(QtCore.QRect(10, 40, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(30)
        self.label_Vnetm.setFont(font)
        self.label_Vnetm.setStyleSheet("border:0px;\n" "background-color:transparent;")
        self.label_Vnetm.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_Vnetm.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vnetm.setObjectName("label_Vnetm")
        self.horizontalLayout_5.addWidget(self.widget)
        self.widget_7 = QtWidgets.QWidget(self.layoutWidget1)
        self.widget_7.setMaximumSize(QtCore.QSize(122, 65))
        self.widget_7.setStyleSheet(
            "background-color:rgb(255, 255, 255);\n"
            "border:1px solid black;\n"
            "border-radius:20px;"
        )
        self.widget_7.setObjectName("widget_7")
        self.label_mrp = QtWidgets.QLabel(self.widget_7)
        self.label_mrp.setEnabled(True)
        self.label_mrp.setGeometry(QtCore.QRect(10, 10, 100, 20))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_mrp.sizePolicy().hasHeightForWidth())
        self.label_mrp.setSizePolicy(sizePolicy)
        self.label_mrp.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Emoji")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_mrp.setFont(font)
        self.label_mrp.setAutoFillBackground(False)
        self.label_mrp.setStyleSheet("border:0px;")
        self.label_mrp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_mrp.setObjectName("label_mrp")
        self.label_Vmrp = QtWidgets.QLabel(self.widget_7)
        self.label_Vmrp.setGeometry(QtCore.QRect(10, 30, 100, 29))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_Vmrp.setFont(font)
        self.label_Vmrp.setStyleSheet("border:0px;")
        self.label_Vmrp.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_Vmrp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vmrp.setObjectName("label_Vmrp")
        self.horizontalLayout_5.addWidget(self.widget_7)
        self.verticalLayout_12.addLayout(self.horizontalLayout_5)
        self.widget_8 = QtWidgets.QWidget(self.main_frame)
        self.widget_8.setGeometry(QtCore.QRect(320, 450, 541, 141))
        self.widget_8.setObjectName("widget_8")
        self.status_text_box = QtWidgets.QTextBrowser(self.widget_8)
        self.status_text_box.setGeometry(QtCore.QRect(10, 10, 531, 101))
        self.status_text_box.setObjectName("status_text_box")
        self.progressBar = QtWidgets.QProgressBar(self.widget_8)
        self.progressBar.setGeometry(QtCore.QRect(180, 120, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 879, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setStyleSheet("")
        self.menuFile.setObjectName("menuFile")
        self.menuDatabase = QtWidgets.QMenu(self.menubar)
        self.menuDatabase.setStyleSheet("")
        self.menuDatabase.setObjectName("menuDatabase")
        self.menuBom = QtWidgets.QMenu(self.menuDatabase)
        self.menuBom.setObjectName("menuBom")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setStyleSheet("")
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionCreateBom = QtGui.QAction(MainWindow)
        self.actionCreateBom.setObjectName("actionCreateBom")
        self.actionUpdate_Existing_Charges = QtGui.QAction(MainWindow)
        self.actionUpdate_Existing_Charges.setObjectName(
            "actionUpdate_Existing_Charges"
        )
        self.actionUpdate_Existing_Price = QtGui.QAction(MainWindow)
        self.actionUpdate_Existing_Price.setObjectName("actionUpdate_Existing_Price")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionUpdateOsCharges = QtGui.QAction(MainWindow)
        self.actionUpdateOsCharges.setObjectName("actionUpdateOsCharges")
        self.actionUpdatePriceStructure = QtGui.QAction(MainWindow)
        self.actionUpdatePriceStructure.setObjectName("actionUpdatePriceStructure")
        self.actionCreateOsCharges = QtGui.QAction(MainWindow)
        self.actionCreateOsCharges.setObjectName("actionCreateOsCharges")
        self.actionCreatePriceStructure = QtGui.QAction(MainWindow)
        self.actionCreatePriceStructure.setObjectName("actionCreatePriceStructure")
        self.menuFile.addAction(self.actionClose)
        self.menuBom.addAction(self.actionCreateBom)
        self.menuBom.addAction(self.actionCreateOsCharges)
        self.menuBom.addAction(self.actionCreatePriceStructure)
        self.menuDatabase.addAction(self.actionUpdateOsCharges)
        self.menuDatabase.addAction(self.actionUpdatePriceStructure)
        self.menuDatabase.addAction(self.menuBom.menuAction())
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # Core Functionalities
        self.progressBar.hide()
        self.button_show_stats.clicked.connect(self.buttonShow)
        self.button_export_xl.clicked.connect(self.buttonExport)
        self.button_export_summary.clicked.connect(self.buttonExportSummaryReport)
        # TODO: Create new method
        self.button_export_xl_sub.clicked.connect(self.buttonExport)

        # Menu items
        self.actionCreateBom.triggered.connect(self.menu_create_bom)
        self.actionCreateOsCharges.triggered.connect(self.menu_create_osc)
        self.actionCreatePriceStructure.triggered.connect(self.menu_create_ps)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Fortune Br - Bill of Materials")
        )
        self.button_show_stats.setText(_translate("MainWindow", "Show Stats"))
        self.button_export_xl.setText(_translate("MainWindow", "Export"))
        self.button_export_summary.setText(_translate("MainWindow", "Report"))
        self.label.setText(_translate("MainWindow", "DG9110 Navy Blue Red Gents"))
        self.label_stich.setText(_translate("MainWindow", "Stitching Charge"))
        self.label_Vstitch.setText(_translate("MainWindow", "0.00"))
        self.label_print.setText(_translate("MainWindow", "Printing Charge"))
        self.label_Vprint.setText(_translate("MainWindow", "0.00"))
        self.label_mc.setText(_translate("MainWindow", "Material Cost"))
        self.label_Vmc.setText(_translate("MainWindow", "0.00"))
        self.label_cop.setText(_translate("MainWindow", "Cost of Production"))
        self.label_Vcop.setText(_translate("MainWindow", "0.00"))
        self.label_Vbasic.setText(_translate("MainWindow", "0.00"))
        self.label_basic.setText(_translate("MainWindow", "BASIC"))
        self.label_netm.setText(_translate("MainWindow", "Net Margin"))
        self.label_Vnetm.setText(_translate("MainWindow", "-00.00%"))
        self.label_mrp.setText(_translate("MainWindow", "MRP"))
        self.label_Vmrp.setText(_translate("MainWindow", "0.00"))
        self.status_text_box.setHtml(
            _translate(
                "MainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                # '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Slack-Lato,appleLogo,sans-serif\'; color:#000000;">( ＾∇＾)</span><span style=" font-size:10pt;"> Specially deddicated to </span><span style=" font-size:10pt; font-weight:600; color:#5555ff;">Manaf K N </span><span style=" font-size:10pt; font-weight:600; color:#000000;">- UMC</span></p>\n'
                # '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
                "<br/><br/><br/>\n"
                '<p align="right" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:10pt; font-style:italic; background-color:#ffffff;">Made with </span><span style=" font-family:\'apple color emoji,segoe ui emoji,noto color emoji,android emoji,emojisymbols,emojione mozilla,twemoji mozilla,segoe ui symbol\'; font-size:10pt; color:#ff0000; background-color:#ffffff;">❤️</span><span style=" font-size:10pt; font-style:italic; background-color:#ffffff;"> from </span><span style=" font-size:10pt; font-weight:600; font-style:italic; background-color:#ffffff;">OM</span><span style=" font-size:10pt; font-style:italic; background-color:#ffffff;"> Dept - Fortune Branch </span></p></body></html>',
            )
        )
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDatabase.setTitle(_translate("MainWindow", "Database"))
        self.menuBom.setTitle(_translate("MainWindow", "Re-create Tables"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionCreateBom.setText(_translate("MainWindow", "Bom"))
        self.actionUpdate_Existing_Charges.setText(
            _translate("MainWindow", "Update Existing Charges")
        )

        self.actionUpdate_Existing_Price.setText(
            _translate("MainWindow", "Update Existing Price")
        )

        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionUpdateOsCharges.setText(
            _translate("MainWindow", "Manage OS Charges")
        )
        self.actionUpdatePriceStructure.setText(
            _translate("MainWindow", "Manage Price Structure")
        )
        self.actionCreateOsCharges.setText(_translate("MainWindow", "OS Charges"))
        self.actionCreatePriceStructure.setText(
            _translate("MainWindow", "Price Structure")
        )

    def tableSelectAll(self):
        """Select or Unselect all check boxes in the table.

        Table View corner button function.
        """
        if self.is_all_selected:
            self.tableView.clearSelection()
        self.is_all_selected = not self.is_all_selected

    def tableDoubleClicked(self, *args):
        """Double clicked item in the tableview.

        Same effect as buttonShow: will shows the stats
        """
        self.buttonShow()

    def tableSelectionChanged(
        self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection
    ):
        """Catch Selection changed behaviour"""
        for item in selected.indexes():
            self.model.item(item.row(), 0).setCheckState(Qt.CheckState.Checked)
        for item in deselected.indexes():
            self.model.item(item.row(), 0).setCheckState(Qt.CheckState.Unchecked)

    def tableSingleClicked(self, modelIndex: QtCore.QModelIndex):
        """Single clicked item in the tableview.

        Select or Unselect item.
        """
        if (
            self.model.item(modelIndex.row(), 0).checkState() == Qt.CheckState.Checked
            and modelIndex not in self.tableView.selectedIndexes()
        ) or (
            self.model.item(modelIndex.row(), 0).checkState() == Qt.CheckState.Unchecked
            and modelIndex in self.tableView.selectedIndexes()
        ):

            self.tableView.selectionModel().select(
                modelIndex, QtCore.QItemSelectionModel.SelectionFlag.Toggle
            )

    def buttonShow(self):
        """Shows cost data"""
        self.default_label_values()
        selection = self.tableView.selectedIndexes()
        if len(selection) == 1:
            key = self.tableView.model().data(selection[0])
            article = self.articles_dict[key][0]
            ps = self.articles_dict[key][1]  # Price Structure
            oc = self.articles_dict[key][2]  # Os Charge
            self.label.setText(article.article)
            if article.mrp > 0:
                self.label_Vmrp.setText(str(article.mrp))

            if ps == None:
                print("No matching basic rate found for the brand mrp")
            else:
                self.label_Vbasic.setText(str(ps.basic))
            if oc == None:
                print("OS charges for the article isn't given.")
            else:
                self.label_Vprint.setText(str(oc.printing))
                self.label_Vstitch.setText(str(oc.stitching))
            if not None in self.articles_dict[key]:
                df = sql_db.query_fetch_bom_df(article.sap_code, article.size)
                if isinstance(df, DataFrame) and not df.empty:
                    bom = BillOfMaterial(df, article.pairs_in_case)
                    result = calculateProfit(
                        basic_rate=ps.basic,
                        os_charges=oc,
                        fixed_rates=self.fixed_rates,
                        material_cost=bom.get_cost_of_materials,
                    )
                    print(result)
                    self.label_Vcop.setText(str(round(result[0], 2)))
                    self.label_Vmc.setText(str(round(bom.get_cost_of_materials, 2)))
                    self.label_Vnetm.setText("{}%".format(round(result[-1], 2)))
                    if result[-1] < 0:
                        self.label_Vnetm.setStyleSheet("color : red;border:0px;")
                    else:
                        self.label_Vnetm.setStyleSheet("color: green;border:0px;")

        elif selection == []:
            print("No articles selected")
        else:
            # TODO: Show last selected article's cost
            print("Too many articles selected, select only one.")

            print(f"Last selected: {self.tableView.model().data(selection[-1])}")

    def buttonExport(self):
        """
        Export button functionality: export as excel file

        """

        selections = self.tableView.selectedIndexes()
        if len(selections) >= 1:
            for selection in selections:
                key = self.tableView.model().data(selection)
                article = self.articles_dict[key][0]
                ps = self.articles_dict[key][1]  # Price Structure
                oc = self.articles_dict[key][2]  # Os Charge

                if ps == None:
                    print(
                        f'No matching basic rate found for the brand mrp of "{article.article}"'
                    )
                    continue

                if oc == None:
                    print(
                        f"""OS charges for the article "{article.article}" isn't given."""
                    )
                    continue

                df = sql_db.query_fetch_bom_df(article.sap_code, article.size)
                if isinstance(df, DataFrame) and not df.empty:
                    bom = BillOfMaterial(df, article.pairs_in_case)
                    xl = ExcelReporting(
                        article,
                        oc,
                        ps.basic,
                        self.fixed_rates,
                        bom.rexine_df,
                        bom.component_df,
                        bom.moulding_df,
                        bom.packing_df,
                    )
                    xl.generateTable()
        else:
            print("No articles selected")

    def buttonExportSummaryReport(self):
        """
        Export all articles cost sheet summary.

        """

        selections = self.tableView.selectedIndexes()
        if len(selections) >= 20:
            data = []
            for selection in selections:
                key = self.tableView.model().data(selection)
                article = self.articles_dict[key][0]
                ps = self.articles_dict[key][1]  # Price Structure
                oc = self.articles_dict[key][2]  # Os Charge

                if ps == None:
                    print(
                        f'No matching basic rate found for the brand mrp of "{article.article}"'
                    )
                    continue

                if oc == None:
                    print(
                        f"""OS charges for the article "{article.article}" isn't given."""
                    )
                    continue

                df = sql_db.query_fetch_bom_df(article.sap_code, article.size)
                if isinstance(df, DataFrame) and not df.empty:
                    bom = BillOfMaterial(df, article.pairs_in_case)

                    data.append(
                        [
                            article.art_no,
                            article.category,
                            article.color,
                            article.article_code,
                            oc.stitch_rate,
                            oc.print_rate,
                            bom.get_cost_of_materials,
                            ps.basic,
                            ps.mrp,
                        ]
                    )
            if len(data) >= 10:
                columns = [
                    "Art No",
                    "Category",
                    "Color",
                    "Sap Code",
                    "Stitching Rate",
                    "Printing Rate",
                    "Cost of Materials",
                    "Basic Rate",
                    "MRP",
                ]
                df = DataFrame(data, columns=columns)
                generate_bulk_report(df, self.fixed_rates)
        else:
            print("Required minimum number of articles is 20 to get the report.")

    # Menu item dialogs
    def menu_create_bom(self):
        if self.menu_items.get("create_bom", None) is None:
            self.menu_items["create_bom"] = WindowCreateBom()
            self.menu_items["create_bom"].show()
            self.menu_items["create_bom"].close_window.connect(
                self.close_create_bom_menu
            )

    def close_create_bom_menu(self):
        if self.menu_items.get("create_bom", None) != None:
            self.menu_items["create_bom"] = None

    def menu_create_osc(self):
        if self.menu_items.get("create_osc", None) is None:
            self.menu_items["create_osc"] = WindowCreateOsCharges()
            self.menu_items["create_osc"].show()
            self.menu_items["create_osc"].close_window.connect(
                self.close_create_osc_menu
            )

    def close_create_osc_menu(self):
        if self.menu_items.get("create_osc", None) != None:
            self.menu_items["create_osc"] = None

    def menu_create_ps(self):
        if self.menu_items.get("create_ps", None) is None:
            self.menu_items["create_ps"] = WindowCreatePriceStructure()
            self.menu_items["create_ps"].show()
            self.menu_items["create_ps"].close_window.connect(self.close_create_ps_menu)

    def close_create_ps_menu(self):
        if self.menu_items.get("create_ps", None) != None:
            self.menu_items["create_ps"] = None

    def default_label_values(self):
        """Clear all values in labels"""

        self.label_Vstitch.setText("--")
        self.label_Vprint.setText("--")
        self.label_Vmc.setText("--")
        self.label_Vcop.setText("--")
        self.label_Vmrp.setText("--")
        self.label_Vbasic.setText("--")
        self.label_Vnetm.setText("--")
        self.label_Vnetm.setStyleSheet("color : black;border:0px;")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
