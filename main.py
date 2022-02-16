from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from core.calculate_bom import BillOfMaterial
from pandas import DataFrame
from core.cost_analysis import calculateProfit, generate_bulk_report
from core.create_excel_report import ExcelReporting

# from PyQt6.QtCore import Qt, QSortFilterProxyModel
# from PyQt6.QtGui import QStandardItemModel, QStandardItem

from database import sql_db
from database.sql_db import PriceStructure, OSCharges, Article


class Ui_MainWindow(object):
    def __init__(self) -> None:
        super().__init__()

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
        MainWindow.resize(800, 600)
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
            ""
        )

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(
            "QPushButton::pressed {  background:rgb(144, 198, 255) }\n" ""
        )
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 30, 341, 461))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.textChanged.connect(
            self.filter_proxy_model.setFilterRegularExpression
        )
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.tableView = QtWidgets.QTableView(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setMinimumSize(QtCore.QSize(300, 0))
        self.tableView.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.tableView.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self.tableView.setModel(self.filter_proxy_model)
        # Table Functionality
        self.tableView.doubleClicked.connect(self.tableDoubleClicked)
        self.tableView.clicked.connect(self.tableSingleClicked)
        self.tableView.selectionModel().selectionChanged.connect(
            self.tableSelectionChanged
        )
        # self.tableView.
        self.tableView.findChild(QtWidgets.QAbstractButton).clicked.connect(
            self.tableSelectAll
        )
        self.verticalLayout_2.addWidget(self.tableView)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(420, 20, 308, 82))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_1 = QtWidgets.QPushButton(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_1.sizePolicy().hasHeightForWidth())
        self.pushButton_1.setSizePolicy(sizePolicy)
        self.pushButton_1.setMinimumSize(QtCore.QSize(150, 60))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.pushButton_1.setObjectName("pushButton_1")
        self.horizontalLayout.addWidget(self.pushButton_1)
        self.pushButton_1.clicked.connect(self.buttonShow)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 60))
        self.pushButton_2.clicked.connect(self.buttonExport)
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(430, 130, 301, 351))
        self.widget2.setObjectName("widget2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_sth = QtWidgets.QLabel(self.widget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sth.sizePolicy().hasHeightForWidth())
        self.label_sth.setSizePolicy(sizePolicy)
        self.label_sth.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_sth.setFont(font)
        self.label_sth.setStyleSheet("background-color:rgb(217, 255, 215)")
        self.label_sth.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_sth.setObjectName("label_sth")
        self.gridLayout.addWidget(self.label_sth, 0, 0, 1, 1)
        self.label_Vstitch = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Vstitch.setFont(font)
        self.label_Vstitch.setStyleSheet("background-color:rgb(217, 255, 215)")
        self.label_Vstitch.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_Vstitch.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vstitch.setObjectName("label_Vstitch")
        self.gridLayout.addWidget(self.label_Vstitch, 0, 1, 1, 1)
        self.label_print = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_print.setFont(font)
        self.label_print.setStyleSheet("background-color:rgb(217, 255, 215)")
        self.label_print.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_print.setObjectName("label_print")
        self.gridLayout.addWidget(self.label_print, 1, 0, 1, 1)
        self.label_Vprint = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Vprint.setFont(font)
        self.label_Vprint.setStyleSheet("background-color:rgb(217, 255, 215)")
        self.label_Vprint.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vprint.setObjectName("label_Vprint")
        self.gridLayout.addWidget(self.label_Vprint, 1, 1, 1, 1)
        self.label_mrp = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_mrp.setFont(font)
        self.label_mrp.setStyleSheet("background-color:rgb(229, 255, 190)")
        self.label_mrp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_mrp.setObjectName("label_mrp")
        self.gridLayout.addWidget(self.label_mrp, 2, 0, 1, 1)
        self.label_Vmrp = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Vmrp.setFont(font)
        self.label_Vmrp.setStyleSheet("background-color:rgb(229, 255, 190)")
        self.label_Vmrp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vmrp.setObjectName("label_Vmrp")
        self.gridLayout.addWidget(self.label_Vmrp, 2, 1, 1, 1)
        self.label_basic = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_basic.setFont(font)
        self.label_basic.setStyleSheet("background-color:rgb(229, 255, 190)")
        self.label_basic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_basic.setObjectName("label_basic")
        self.gridLayout.addWidget(self.label_basic, 3, 0, 1, 1)
        self.label_Vbasic = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Vbasic.setFont(font)
        self.label_Vbasic.setStyleSheet("background-color:rgb(229, 255, 190)")
        self.label_Vbasic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vbasic.setObjectName("label_Vbasic")
        self.gridLayout.addWidget(self.label_Vbasic, 3, 1, 1, 1)
        self.label_cop = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_cop.setFont(font)
        self.label_cop.setStyleSheet("background-color:rgb(227, 255, 185)")
        self.label_cop.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_cop.setObjectName("label_cop")
        self.gridLayout.addWidget(self.label_cop, 4, 0, 1, 1)
        self.label_Vcop = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Vcop.setFont(font)
        self.label_Vcop.setStyleSheet("background-color:rgb(227, 255, 185)")
        self.label_Vcop.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vcop.setObjectName("label_Vcop")
        self.gridLayout.addWidget(self.label_Vcop, 4, 1, 1, 1)
        self.label_netm = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_netm.setFont(font)
        self.label_netm.setStyleSheet("background-color:rgb(240, 255, 160)")
        self.label_netm.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_netm.setObjectName("label_netm")
        self.gridLayout.addWidget(self.label_netm, 5, 0, 1, 1)
        self.label_Vnetm = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_Vnetm.setFont(font)
        self.label_Vnetm.setStyleSheet("background-color:rgb(240, 255, 160)")
        self.label_Vnetm.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Vnetm.setObjectName("label_Vnetm")
        self.gridLayout.addWidget(self.label_Vnetm, 5, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setStyleSheet("")
        self.menuFile.setObjectName("menuFile")
        self.menuDatabase = QtWidgets.QMenu(self.menubar)
        self.menuDatabase.setStyleSheet("")
        self.menuDatabase.setObjectName("menuDatabase")
        self.menuBom = QtWidgets.QMenu(self.menuDatabase)
        self.menuBom.setObjectName("menuBom")
        self.menuOS_Charges = QtWidgets.QMenu(self.menuDatabase)
        self.menuOS_Charges.setObjectName("menuOS_Charges")
        self.menuPrice_Structure = QtWidgets.QMenu(self.menuDatabase)
        self.menuPrice_Structure.setObjectName("menuPrice_Structure")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setStyleSheet("")
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionUpdate_From_File = QtGui.QAction(MainWindow)
        self.actionUpdate_From_File.setObjectName("actionUpdate_From_File")
        self.actionAdd_New_Charges = QtGui.QAction(MainWindow)
        self.actionAdd_New_Charges.setObjectName("actionAdd_New_Charges")
        self.actionUpdate_Existing_Charges = QtGui.QAction(MainWindow)
        self.actionUpdate_Existing_Charges.setObjectName(
            "actionUpdate_Existing_Charges"
        )
        self.actionUpdate_From_File_2 = QtGui.QAction(MainWindow)
        self.actionUpdate_From_File_2.setObjectName("actionUpdate_From_File_2")
        self.actionAdd_New_Price = QtGui.QAction(MainWindow)
        self.actionAdd_New_Price.setObjectName("actionAdd_New_Price")
        self.actionUpdate_Existing_Price = QtGui.QAction(MainWindow)
        self.actionUpdate_Existing_Price.setObjectName("actionUpdate_Existing_Price")
        self.actionUpdate_From_File_3 = QtGui.QAction(MainWindow)
        self.actionUpdate_From_File_3.setObjectName("actionUpdate_From_File_3")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionClose)
        self.menuBom.addAction(self.actionUpdate_From_File)
        self.menuOS_Charges.addAction(self.actionAdd_New_Charges)
        self.menuOS_Charges.addAction(self.actionUpdate_Existing_Charges)
        self.menuOS_Charges.addSeparator()
        self.menuOS_Charges.addAction(self.actionUpdate_From_File_2)
        self.menuPrice_Structure.addAction(self.actionAdd_New_Price)
        self.menuPrice_Structure.addAction(self.actionUpdate_Existing_Price)
        self.menuPrice_Structure.addSeparator()
        self.menuPrice_Structure.addAction(self.actionUpdate_From_File_3)
        self.menuDatabase.addAction(self.menuBom.menuAction())
        self.menuDatabase.addAction(self.menuOS_Charges.menuAction())
        self.menuDatabase.addAction(self.menuPrice_Structure.menuAction())
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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

        selection = self.tableView.selectedIndexes()
        if len(selection) == 1:
            key = self.tableView.model().data(selection[0])
            article = self.articles_dict[key][0]
            ps = self.articles_dict[key][1]  # Price Structure
            oc = self.articles_dict[key][2]  # Os Charge

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
                    self.label_Vnetm.setText("{} %".format(round(result[-1], 2)))
                    if result[-1] < 0:
                        self.label_Vnetm.setStyleSheet(
                            "color : red;background-color:rgb(240, 255, 160);"
                        )
                    else:
                        self.label_Vnetm.setStyleSheet(
                            "color: green;background-color:rgb(240, 255, 160);"
                        )

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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Fortune Br - Bill of Materials")
        )
        self.pushButton_1.setText(_translate("MainWindow", "Show"))
        self.pushButton_2.setText(_translate("MainWindow", "Export"))
        self.label_sth.setText(_translate("MainWindow", "Stitching Charge"))
        self.label_Vstitch.setText(_translate("MainWindow", "0.00"))
        self.label_print.setText(_translate("MainWindow", "Printing Charge"))
        self.label_Vprint.setText(_translate("MainWindow", "0.00"))
        self.label_mrp.setText(_translate("MainWindow", "MRP"))
        self.label_Vmrp.setText(_translate("MainWindow", "0.00"))
        self.label_basic.setText(_translate("MainWindow", "BASIC"))
        self.label_Vbasic.setText(_translate("MainWindow", "0.00"))
        self.label_cop.setText(_translate("MainWindow", "Cost of Production"))
        self.label_Vcop.setText(_translate("MainWindow", "0.00"))
        self.label_netm.setText(_translate("MainWindow", "Net Margin"))
        self.label_Vnetm.setText(_translate("MainWindow", "0.00"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDatabase.setTitle(_translate("MainWindow", "Database"))
        self.menuBom.setTitle(_translate("MainWindow", "Bom"))
        self.menuOS_Charges.setTitle(_translate("MainWindow", "OS Charges"))
        self.menuPrice_Structure.setTitle(_translate("MainWindow", "Price Structure"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionUpdate_From_File.setText(
            _translate("MainWindow", "Update From File")
        )
        self.actionAdd_New_Charges.setText(_translate("MainWindow", "Add New Charges"))
        self.actionUpdate_Existing_Charges.setText(
            _translate("MainWindow", "Update Existing Charges")
        )
        self.actionUpdate_From_File_2.setText(
            _translate("MainWindow", "Update From File")
        )
        self.actionAdd_New_Price.setText(_translate("MainWindow", "Add New Price"))
        self.actionUpdate_Existing_Price.setText(
            _translate("MainWindow", "Update Existing Price")
        )
        self.actionUpdate_From_File_3.setText(
            _translate("MainWindow", "Update From File")
        )
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
