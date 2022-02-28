from pandas import DataFrame
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from core.utils.calculate_bom import BillOfMaterial
from core.utils.cost_analysis import calculateProfit, generate_bulk_report
from core.utils.create_excel_report import ExcelReporting
from database import sql_db
from database.database import PriceStructure, OSCharges, Article
from ui.ui_main_window import Ui_MainWindow
from windows.window_create_bom import WindowCreateBom
from windows.window_create_osc import WindowCreateOsCharges
from windows.window_create_ps import WindowCreatePriceStructure
from windows.window_manage_osc import WindowManageOsCharges
from windows.window_manage_ps import WindowManagePriceStructure


class WindowHomeScreen(QtWidgets.QMainWindow):
    """Main Screen of the application"""

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.menu_items = {}
        self.is_all_selected = False  # Table items
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()

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
        self.filter_proxy_model.setSourceModel(self.model)
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
        self.ui.button_show_stats.clicked.connect(self.buttonShow)
        self.ui.button_export_xl.clicked.connect(self.buttonExport)
        self.ui.button_export_summary.clicked.connect(self.buttonExportSummaryReport)
        # TODO: Create new method to export only currently displaying item
        self.ui.button_export_xl_sub.clicked.connect(self.buttonExport)

        # Connections to menu items
        self.ui.actionClose.triggered.connect(self.menu_close_app)
        self.ui.actionUpgradeBom.triggered.connect(self.menu_create_bom)
        self.ui.actionUpgradeOS_Charge.triggered.connect(self.menu_create_osc)
        self.ui.actionUpgradePrice_Structure.triggered.connect(self.menu_create_ps)
        self.ui.actionUpdateOS_Charges.triggered.connect(self.menu_manage_osc)
        self.ui.actionUpdatePrice_Structure.triggered.connect(self.menu_manage_ps)

    def tableSelectAll(self):
        """Select or Unselect all check boxes in the table

        Table View corner button function.
        """
        if self.is_all_selected:
            self.ui.tableView.clearSelection()
        self.is_all_selected = not self.is_all_selected

    def tableDoubleClicked(self, *args):
        """Double clicked item in the tableview

        Same effect as buttonShow: will shows the stats.
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
        """Single clicked item in the tableview

        Select or Unselect item.
        """
        if (
            self.model.item(modelIndex.row(), 0).checkState() == Qt.CheckState.Checked
            and modelIndex not in self.ui.tableView.selectedIndexes()
        ) or (
            self.model.item(modelIndex.row(), 0).checkState() == Qt.CheckState.Unchecked
            and modelIndex in self.ui.tableView.selectedIndexes()
        ):

            self.ui.tableView.selectionModel().select(
                modelIndex, QtCore.QItemSelectionModel.SelectionFlag.Toggle
            )

    def buttonShow(self):
        """Shows cost data"""

        self.default_label_values()
        selection = self.ui.tableView.selectedIndexes()
        if len(selection) == 1:
            key = self.ui.tableView.model().data(selection[0])
            article = self.articles_dict[key][0]
            ps = self.articles_dict[key][1]  # Price Structure
            oc = self.articles_dict[key][2]  # Os Charge
            self.ui.label_article.setText(article.article)
            if article.mrp > 0:
                self.ui.label_Vmrp.setText(str(article.mrp))

            if ps == None:
                print("No matching basic rate found for the brand mrp")
            else:
                self.ui.label_Vbasic.setText(str(ps.basic))
            if oc == None:
                print("OS charges for the article isn't given.")
            else:
                self.ui.label_Vprint.setText(str(oc.printing))
                self.ui.label_Vstitch.setText(str(oc.stitching))
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
                    self.ui.label_Vcop.setText(str(round(result[0], 2)))
                    self.ui.label_Vmc.setText(str(round(bom.get_cost_of_materials, 2)))
                    self.ui.label_Vnetm.setText("{}%".format(round(result[-1], 2)))
                    if result[-1] < 0:
                        self.ui.label_Vnetm.setStyleSheet("color : red;border:0px;")
                    else:
                        self.ui.label_Vnetm.setStyleSheet("color: green;border:0px;")

        elif selection == []:
            print("No articles selected")
        else:
            # TODO: Show last selected article's cost
            print("Too many articles selected, select only one.")

            print(f"Last selected: {self.ui.tableView.model().data(selection[-1])}")

    def buttonExport(self):
        """
        Export button functionality: export as excel file

        """

        selections = self.ui.tableView.selectedIndexes()
        if len(selections) >= 1:
            for selection in selections:
                key = self.ui.tableView.model().data(selection)
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

        selections = self.ui.tableView.selectedIndexes()
        if len(selections) >= 20:
            data = []
            for selection in selections:
                key = self.ui.tableView.model().data(selection)
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

    # Menu item functions
    def menu_close_app(self):
        QtCore.QCoreApplication.instance().quit()

    def menu_create_bom(self):
        if self.menu_items.get("create_bom", None) is None:
            self.menu_items["create_bom"] = WindowCreateBom()
            self.menu_items["create_bom"].show()
            self.menu_items["create_bom"].close_window.connect(
                self.menu_close_create_bom
            )

    def menu_close_create_bom(self):
        if self.menu_items.get("create_bom", None) != None:
            self.menu_items["create_bom"] = None

    def menu_create_osc(self):
        if self.menu_items.get("create_osc", None) is None:
            self.menu_items["create_osc"] = WindowCreateOsCharges()
            self.menu_items["create_osc"].show()
            self.menu_items["create_osc"].close_window.connect(
                self.menu_close_create_osc
            )

    def menu_close_create_osc(self):
        if self.menu_items.get("create_osc", None) != None:
            self.menu_items["create_osc"] = None

    def menu_create_ps(self):
        if self.menu_items.get("create_ps", None) is None:
            self.menu_items["create_ps"] = WindowCreatePriceStructure()
            self.menu_items["create_ps"].show()
            self.menu_items["create_ps"].close_window.connect(self.close_create_ps_menu)

    def menu_manage_osc(self):
        if self.menu_items.get("manage_osc", None) is None:
            self.menu_items["manage_osc"] = WindowManageOsCharges()
            self.menu_items["manage_osc"].show()
            self.menu_items["manage_osc"].close_window.connect(
                self.menu_close_manage_osc
            )

    def menu_close_manage_osc(self):
        if self.menu_items.get("manage_osc", None) != None:
            self.menu_items["manage_osc"] = None

    def menu_manage_ps(self):
        if self.menu_items.get("manage_ps", None) is None:
            self.menu_items["manage_ps"] = WindowManagePriceStructure()
            self.menu_items["manage_ps"].show()
            self.menu_items["manage_ps"].close_window.connect(self.menu_close_manage_ps)

    def menu_close_manage_ps(self):
        if self.menu_items.get("manage_ps", None) != None:
            self.menu_items["manage_ps"] = None

    def close_create_ps_menu(self):
        if self.menu_items.get("create_ps", None) != None:
            self.menu_items["create_ps"] = None

    def default_label_values(self):
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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    MainWindow = WindowHomeScreen()
    MainWindow.show()
    sys.exit(app.exec())
