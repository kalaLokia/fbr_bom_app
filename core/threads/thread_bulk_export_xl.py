import math
from typing import TYPE_CHECKING

import pandas as pd
from PyQt6 import QtCore

from core.utils.calculate_bom import BillOfMaterial
from core.utils.cost_analysis import generate_bulk_report
from core.utils.create_excel_report import ExcelReporting
from database.sql_db import query_fetch_bom_df


if TYPE_CHECKING:
    from database.database import Article, PriceStructure, OSCharges


class WorkerThreadXlExport(QtCore.QThread):
    """Thread to export multiple articles bom report in excel format"""

    completed = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int)
    error_log = QtCore.pyqtSignal(str)

    def __init__(
        self,
        articles_data: list[tuple["Article", "PriceStructure", "OSCharges"]],
        fixed_rates,
        path: str = None,
    ) -> None:
        super(QtCore.QThread, self).__init__()

        self.articles_data = articles_data
        self.fixed_rates = fixed_rates
        self.path = path

    def run(self) -> None:
        """Run task in thread"""

        # Show the status application
        success_count = 0
        count = 0
        total_count = len(self.articles_data)
        for article, ps, oc in self.articles_data:
            self.progress.emit(math.trunc(count / total_count * 100))
            count += 1
            basic_rate = 0
            if ps == None:
                self.error_log.emit(
                    f'No matching basic rate found for "{article.brand} - {article.mrp}".'
                )
                # Show as warning
            else:
                basic_rate = ps.basic

            if oc == None:
                self.error_log.emit(
                    f"""OS charges for the article "{article.article}" isn't given. Skipping..."""
                )
                # Show as skipped
                continue

            df = query_fetch_bom_df(article.sap_code, article.size)
            if isinstance(df, pd.DataFrame) and not df.empty:
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
                xl.generateTable(filepath=self.path)
                success_count += 1

        self.progress.emit(100)
        self.completed.emit(success_count)


class WorkerThreadXlExportSummary(QtCore.QThread):
    """Thread to export multiple articles bom report in excel format"""

    completed = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int)
    error_log = QtCore.pyqtSignal(str)

    def __init__(
        self,
        articles_data: list[tuple["Article", "PriceStructure", "OSCharges"]],
        fixed_rates,
        filename: str = None,
    ) -> None:
        super(QtCore.QThread, self).__init__()

        self.articles_data = articles_data
        self.fixed_rates = fixed_rates
        self.filename = filename

    def run(self) -> None:
        """Run task in thread"""

        # Show the status application
        success_count = 0
        data = []
        count = 0
        total_count = len(self.articles_data)
        for article, ps, oc in self.articles_data:
            self.progress.emit(math.trunc(count / total_count * 100))
            count += 1
            if ps == None:
                self.error_log.emit(
                    f'No matching basic rate found for "{article.brand} - {article.mrp}". Skipping {article.article}'
                )
                continue

            if oc == None:
                self.error_log.emit(
                    f"""OS charges for the article "{article.article}" isn't given. Skipping..."""
                )

                continue

            df = query_fetch_bom_df(article.sap_code, article.size)
            if isinstance(df, pd.DataFrame) and not df.empty:
                success_count += 1
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
            df = pd.DataFrame(data, columns=columns)
            generate_bulk_report(df, self.fixed_rates, self.filename)

        else:
            self.progress.emit(0)
            self.completed.emit(0)
            return
        self.progress.emit(100)
        self.completed.emit(success_count)
