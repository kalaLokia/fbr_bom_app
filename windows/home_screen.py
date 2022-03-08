import os

from pandas import DataFrame
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from core.threads.thread_bulk_export_xl import (
    WorkerThreadXlExport,
    WorkerThreadXlExportSummary,
)
from core.utils.calculate_bom import BillOfMaterial
from core.utils.cost_analysis import calculateProfit
from core.utils.create_excel_report import ExcelReporting
from database import sql_db
from database.database import PriceStructure, OSCharges, Article
from settings import EXPORT_DIR
from ui.ui_main_window import Ui_MainWindow
from windows.window_create_bom import WindowCreateBom
from windows.window_create_osc import WindowCreateOsCharges
from windows.window_create_ps import WindowCreatePriceStructure
from windows.window_manage_osc import WindowManageOsCharges
from windows.window_manage_ps import WindowManagePriceStructure
from windows.window_manage_expenses import WindowManageExpenses
from windows.window_manage_fixed_rates import WindowManageFixedCharges


class WindowHomeScreen(QtWidgets.QMainWindow):
    """Main Screen of the application"""

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.menu_items = {}
        self.active_article: str = None  # Currently active article displaying
        self.is_all_selected = False  # Table items
        self.ui.widget_status.hide()  # hiding stats page initially
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.articles_dict: dict[str, tuple[Article, PriceStructure, OSCharges]] = {}
        self.refreshDataModel()
        self.filter_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.filter_proxy_model.setFilterKeyColumn(0)

        # Connections with filter
        self.ui.lineEdit.textChanged.connect(
            self.filter_proxy_model.setFilterRegularExpression
        )
        self.ui.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.ui.tableView.setEditTriggers(
            QtWidgets.QTableView.EditTrigger.NoEditTriggers
        )
        self.ui.tableView.setModel(self.filter_proxy_model)
        self.ui.tableView.doubleClicked.connect(self.tableDoubleClicked)
        self.ui.tableView.clicked.connect(self.tableSingleClicked)
        self.ui.tableView.selectionModel().selectionChanged.connect(
            self.tableSelectionChanged
        )
        self.ui.tableView.findChild(QtWidgets.QAbstractButton).clicked.connect(
            self.tableSelectAll
        )

        # Connections to buttons
        self.ui.button_show_stats.clicked.connect(self.buttonShowStats)
        self.ui.button_export_xl.clicked.connect(self.buttonExportBulk)
        self.ui.button_export_summary.clicked.connect(self.buttonExportSummaryReport)
        # TODO: Create new method to export only currently displaying item
        self.ui.button_export_xl_sub.clicked.connect(self.buttonExport)

        # Connections to menu items
        self.ui.actionRefresh.triggered.connect(self.refreshDataModel)
        self.ui.actionClose.triggered.connect(self.menu_close_app)
        self.ui.actionUpgradeBom.triggered.connect(self.menu_create_bom)
        self.ui.actionUpgradeOS_Charge.triggered.connect(self.menu_create_osc)
        self.ui.actionUpgradePrice_Structure.triggered.connect(self.menu_create_ps)
        self.ui.actionUpdateOS_Charges.triggered.connect(self.menu_manage_osc)
        self.ui.actionUpdatePrice_Structure.triggered.connect(self.menu_manage_ps)
        self.ui.actionUpdateOther_Expenses.triggered.connect(self.menu_manage_expenses)
        self.ui.actionUpdateFixed_Charges.triggered.connect(
            self.menu_manage_fixed_charges
        )

    def refreshDataModel(self) -> None:
        """Refresh data from server"""

        articles = sql_db.query_fetch_articles_list()
        self.fixed_rates = sql_db.query_fetch_fixed_rates()
        if articles:
            self.model = QtGui.QStandardItemModel(len(articles), 1)
            self.model.setHorizontalHeaderLabels(["Articles"])
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
        else:
            self.model = None
        self.filter_proxy_model.setSourceModel(self.model)
        self.ui.button_export_xl.setDisabled(False)
        self.ui.button_export_summary.setDisabled(False)

    def tableSelectAll(self) -> None:
        """Select or Unselect all check boxes in the table

        Table View corner button function.
        """
        if self.is_all_selected:
            self.ui.tableView.clearSelection()
        self.is_all_selected = not self.is_all_selected

    def tableDoubleClicked(self, *args) -> None:
        """Double clicked item in the tableview

        Same effect as buttonShow: will shows the stats.
        """
        self.buttonShowStats()

    def tableSelectionChanged(
        self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection
    ) -> None:
        """Catch Selection changed behaviour"""

        for index in selected.indexes():
            self.filter_proxy_model.setData(
                index, Qt.CheckState.Checked, Qt.ItemDataRole.CheckStateRole
            )
        for index in deselected.indexes():
            self.filter_proxy_model.setData(
                index, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole
            )

    def tableSingleClicked(self, modelIndex: QtCore.QModelIndex) -> None:
        """Single item clicked/checked in the tableview

        Select or Unselect item when checkbox is checked or unchecked.

        """
        # CheckState key is 10 in itemData - Not read doc for info
        # check_state will be Qt.CheckState "enum value" when checkbox item is checked.
        # check_state will be Qt.CheckState "enum" when item selected.
        # only checkbox item selection is needed, so integer value will consider in here and other ignored which isn't needed.
        check_state = self.filter_proxy_model.itemData(modelIndex).get(10)
        if (
            check_state == 2 and modelIndex not in self.ui.tableView.selectedIndexes()
        ) or (check_state == 0 and modelIndex in self.ui.tableView.selectedIndexes()):
            self.ui.tableView.selectionModel().select(
                modelIndex, QtCore.QItemSelectionModel.SelectionFlag.Toggle
            )

    def buttonShowStats(self) -> None:
        """Shows cost data"""

        if not self.ui.widget_status.isVisible():
            self.ui.widget_status.show()
        self.default_label_values()
        selection = self.ui.tableView.selectedIndexes()
        if len(selection) >= 1:
            # Stats of last selected item
            basic_rate = 0
            self.ui.button_show_stats.setDisabled(True)  # Disable button
            key = self.ui.tableView.model().data(selection[-1])
            self.active_article = key
            article = self.articles_dict[key][0]
            ps = self.articles_dict[key][1]  # Price Structure
            oc = self.articles_dict[key][2]  # Os Charge
            self.ui.label_article.setText(article.article)
            if article.mrp > 0:
                self.ui.label_Vmrp.setText(str(article.mrp))

            if ps == None:
                if article.mrp > 0:
                    reply_yes = self.eventConfirmationDialog(
                        "Missing Basic Rate!",
                        "Do you want to add a new price structure?",
                    )
                    if reply_yes:
                        self.ui.button_show_stats.setDisabled(False)
                        self.menu_manage_ps()
                        ps = "Pride"
                        if article.brand.lower() == "debongo":
                            ps = "Debongo"
                        elif article.brand.lower() == "stile":
                            ps = "Stile"
                        self.menu_items["manage_ps"].ui.combo_structure.setCurrentText(
                            ps
                        )
                        self.menu_items["manage_ps"].ui.text_mrp.setText(
                            str(round(article.mrp, 2))
                        )
                        return
            else:
                basic_rate = ps.basic
                self.ui.label_Vbasic.setText(str(basic_rate))

            # OSCharge missing
            if oc == None:
                reply_yes = self.eventConfirmationDialog(
                    "Missing OSCharges!",
                    f'OS Charge is mandatory, do you want to add the missing OS-charge for "{article.article_code}" now?',
                )

                if reply_yes:
                    self.menu_manage_osc()
                    self.menu_items["manage_osc"].ui.text_article.setText(
                        article.article_code
                    )
                    self.menu_items["manage_osc"].ui.text_print_rate.setText("0.0")
                    self.menu_items["manage_osc"].ui.text_stitch_rate.setText("0.0")

                self.ui.button_show_stats.setDisabled(False)
                return
            else:
                self.ui.label_Vprint.setText(str(oc.printing))
                self.ui.label_Vstitch.setText(str(oc.stitching))

            # if not None in self.articles_dict[key]:
            df = sql_db.query_fetch_bom_df(article.sap_code, article.size)
            if isinstance(df, DataFrame) and not df.empty:
                bom = BillOfMaterial(df, article.pairs_in_case)
                result = calculateProfit(
                    basic_rate=basic_rate,
                    os_charges=oc,
                    fixed_rates=self.fixed_rates,
                    material_cost=bom.get_cost_of_materials,
                )
                print(result)
                result_netm = round(result[-1], 2)
                self.ui.label_Vcop.setText(str(round(result[0], 2)))
                self.ui.label_Vmc.setText(str(round(bom.get_cost_of_materials, 2)))
                if result_netm < 0:
                    self.ui.label_Vnetm.setText("{}%".format(result_netm))
                    self.ui.label_Vnetm.setStyleSheet("color : red;border:0px;")
                elif result_netm == 0 and basic_rate == 0:
                    self.ui.label_Vnetm.setText("NA")
                    self.ui.label_Vnetm.setStyleSheet("color : grey;border:0px;")
                else:
                    self.ui.label_Vnetm.setText("{}%".format(result_netm))
                    self.ui.label_Vnetm.setStyleSheet("color: green;border:0px;")

            self.ui.button_show_stats.setDisabled(False)
        else:
            print("No articles selected")

    def buttonExport(self, key: str = None) -> None:
        """
        Export single article report in excel format.

        """

        selections = self.ui.tableView.selectedIndexes()
        if len(selections) <= 0:
            print("No articles selected")
            return

        # Export actively selected article in stats
        # If key is passed, export that
        if not key:
            key = self.active_article
        article = self.articles_dict[key][0]
        ps = self.articles_dict[key][1]  # Price Structure
        oc = self.articles_dict[key][2]  # Os Charge
        basic_rate = 0
        if ps == None:
            print(
                f'No matching basic rate found for the brand mrp of "{article.article}"'
            )
        else:
            basic_rate = ps.basic

        if oc == None:
            reply_yes = self.eventConfirmationDialog(
                "Missing OSCharges!",
                f'OS Charge is mandatory, do you want to add the missing OS-charge for "{article.article_code}" now?',
            )

            if reply_yes:
                self.menu_manage_osc()
                self.menu_items["manage_osc"].ui.text_article.setText(
                    article.article_code
                )
                self.menu_items["manage_osc"].ui.text_print_rate.setText("0.0")
                self.menu_items["manage_osc"].ui.text_stitch_rate.setText("0.0")
            return

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Detailed Report",
            os.pathsep.join(EXPORT_DIR, article.get_filename),
            "Excel Files (*.xlsx)",
        )

        if not filename:
            return
        else:
            if filename.split(".")[-1] != "xlsx":
                filename = filename.split(".")[:-1] + ".xlsx"

        df = sql_db.query_fetch_bom_df(article.sap_code, article.size)
        if isinstance(df, DataFrame) and not df.empty:
            bom = BillOfMaterial(df, article.pairs_in_case)
            xl = ExcelReporting(
                article,
                oc,
                basic_rate,
                self.fixed_rates,
                bom.rexine_df,
                bom.component_df,
                bom.moulding_df,
                bom.packing_df,
            )
            xl.generateTable(filename=filename)
            msg = f"Successfully exported {article.article} 's report."
            # Make it to ask whether open file or not
            self.eventCompletedDialog(msg)

    def buttonExportBulk(self) -> None:
        """
        Export multiple article's report in excel format

        """

        selections = self.ui.tableView.selectedIndexes()
        if len(selections) <= 0:
            print("No articles selected")
            return
        elif len(selections) == 1:
            # Export lastly selected article; which does not requires to be in a thread
            key = self.ui.tableView.model().data(selections[-1])
            self.buttonExport(key)
        else:
            filepath = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Save Reports In", EXPORT_DIR
            )
            if not filepath:
                return

            self.ui.button_export_xl.setDisabled(True)  # Disable button
            selected_articles = []
            for selection in selections:
                key = self.ui.tableView.model().data(selection)
                selected_articles.append(self.articles_dict[key])

            self.worker = WorkerThreadXlExport(
                selected_articles, self.fixed_rates, filepath
            )
            self.worker.start()

            def task_completed(count):
                msg = f"Successfully exported reports for {count} out of {len(selections)} articles."
                self.eventCompletedDialog(msg)
                self.ui.button_export_xl.setDisabled(False)

            self.worker.completed.connect(task_completed)

    def buttonExportSummaryReport(self) -> None:
        """
        Export all articles cost sheet summary (csv).

        """

        selections = self.ui.tableView.selectedIndexes()
        if len(selections) < 10:
            print("Required minimum number of articles is 20 to get the report.")
            self.eventAlertDialog(
                "Too Small Data",
                "Minimum 10 articles are required to generate the summary report.",
            )
            return
        else:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Save Detailed Report",
                os.path.join(EXPORT_DIR, "Cost Analysis Report _fbr.csv"),
                "CSV Files (*.csv)",
            )

            if not filename:
                return
            else:
                # If user entered invalid file type
                if filename.split(".")[-1] != "csv":
                    filename = filename.split(".")[:-1] + ".csv"

            self.ui.button_export_summary.setDisabled(True)  # Disable button
            selected_articles = []
            for selection in selections:
                key = self.ui.tableView.model().data(selection)
                selected_articles.append(self.articles_dict[key])
            self.worker = WorkerThreadXlExportSummary(
                selected_articles, self.fixed_rates, filename
            )
            self.worker.start()

            def task_completed(count):
                msg = f"Successfully exported summary report for {count} out of {len(selections)} articles."
                self.eventCompletedDialog(msg)
                self.ui.button_export_summary.setDisabled(False)

            self.worker.completed.connect(task_completed)

    # Menu item functions
    def menu_close_app(self) -> None:
        QtCore.QCoreApplication.instance().quit()

    def menu_create_bom(self) -> None:
        if self.menu_items.get("create_bom", None) is None:
            self.menu_items["create_bom"] = WindowCreateBom()
            self.menu_items["create_bom"].show()
            self.menu_items["create_bom"].close_window.connect(
                self.menu_close_create_bom
            )

    def menu_close_create_bom(self, db_changed: bool = False) -> None:
        if self.menu_items.get("create_bom", None) != None:
            self.menu_items["create_bom"] = None
        if db_changed:
            self.refreshDataModel()

    def menu_create_osc(self) -> None:
        if self.menu_items.get("create_osc", None) is None:
            self.menu_items["create_osc"] = WindowCreateOsCharges()
            self.menu_items["create_osc"].show()
            self.menu_items["create_osc"].close_window.connect(
                self.menu_close_create_osc
            )

    def menu_close_create_osc(self, db_changed: bool = False) -> None:
        if self.menu_items.get("create_osc", None) != None:
            self.menu_items["create_osc"] = None
        if db_changed:
            self.refreshDataModel()

    def menu_create_ps(self) -> None:
        if self.menu_items.get("create_ps", None) is None:
            self.menu_items["create_ps"] = WindowCreatePriceStructure()
            self.menu_items["create_ps"].show()
            self.menu_items["create_ps"].close_window.connect(self.menu_close_create_ps)

    def menu_close_create_ps(self, db_changed: bool = False) -> None:
        if self.menu_items.get("create_ps", None) != None:
            self.menu_items["create_ps"] = None
        if db_changed:
            self.refreshDataModel()

    def menu_manage_osc(self) -> None:
        if self.menu_items.get("manage_osc", None) is None:
            self.menu_items["manage_osc"] = WindowManageOsCharges()
            self.menu_items["manage_osc"].show()
            self.menu_items["manage_osc"].close_window.connect(
                self.menu_close_manage_osc
            )

    def menu_close_manage_osc(self, db_changed: bool = False) -> None:
        if self.menu_items.get("manage_osc", None) != None:
            self.menu_items["manage_osc"] = None
        if db_changed:
            self.refreshDataModel()

    def menu_manage_ps(self) -> None:
        if self.menu_items.get("manage_ps", None) is None:
            self.menu_items["manage_ps"] = WindowManagePriceStructure()
            self.menu_items["manage_ps"].show()
            self.menu_items["manage_ps"].close_window.connect(self.menu_close_manage_ps)

    def menu_close_manage_ps(self, db_changed: bool = False) -> None:
        if self.menu_items.get("manage_ps", None) != None:
            self.menu_items["manage_ps"] = None
        if db_changed:
            self.refreshDataModel()

    def menu_manage_expenses(self) -> None:
        if self.menu_items.get("manage_expenses", None) is None:
            self.menu_items["manage_expenses"] = WindowManageExpenses()
            self.menu_items["manage_expenses"].show()
            self.menu_items["manage_expenses"].close_window.connect(
                self.menu_close_manage_expenses
            )

    def menu_close_manage_expenses(self, db_changed: bool = False) -> None:
        if self.menu_items.get("manage_expenses", None) != None:
            self.menu_items["manage_expenses"] = None
        if db_changed:
            self.refreshDataModel()

    def menu_manage_fixed_charges(self) -> None:
        if self.menu_items.get("manage_fixed_charges", None) is None:
            self.menu_items["manage_fixed_charges"] = WindowManageFixedCharges()
            self.menu_items["manage_fixed_charges"].show()
            self.menu_items["manage_fixed_charges"].close_window.connect(
                self.menu_close_manage_fixed_charges
            )

    def menu_close_manage_fixed_charges(self, db_changed: bool = False) -> None:
        if self.menu_items.get("manage_fixed_charges", None) != None:
            self.menu_items["manage_fixed_charges"] = None
        if db_changed:
            self.refreshDataModel()

    def default_label_values(self) -> None:
        """Clear all values in labels"""
        self.ui.label_article.setText("0000 Black Gents")
        self.ui.label_Vstitch.setText("--")
        self.ui.label_Vprint.setText("--")
        self.ui.label_Vmc.setText("--")
        self.ui.label_Vcop.setText("--")
        self.ui.label_Vmrp.setText("--")
        self.ui.label_Vbasic.setText("--")
        self.ui.label_Vnetm.setText("--")
        self.ui.label_Vnetm.setStyleSheet("color : black;border:0px;")

    def eventConfirmationDialog(self, title, message) -> bool:
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle(title)
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        dialog.setWindowIcon(QtGui.QIcon("icons/circle-exclamation-solid.svg"))
        dialog.setText(message)
        dialog.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No
        )
        response = dialog.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        return False

    def eventAlertDialog(self, title, message) -> bool:
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle(title)
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
        dialog.setWindowIcon(QtGui.QIcon("icons/triangle-exclamation-solid.svg"))
        dialog.setText(message)
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        response = dialog.exec()

        if response == QtWidgets.QMessageBox.StandardButton.Ok:
            return True
        return False

    def eventCompletedDialog(self, message) -> None:
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Successful")
        dialog.setIcon(QtWidgets.QMessageBox.Icon.NoIcon)
        dialog.setWindowIcon(QtGui.QIcon("icons/favicon.ico"))
        dialog.setText(message)
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        dialog.exec()
