from typing import TYPE_CHECKING

import pandas as pd
from PyQt6 import QtCore

from database.sql_db import query_fetch_bom_df

from core.utils.calculate_bom import BillOfMaterial
from core.utils.create_excel_report import ExcelReporting

if TYPE_CHECKING:
    from database.database import Article, PriceStructure, OSCharges


class WorkerThreadXlExport(QtCore.QThread):
    """Thread to export multiple articles bom report in excel format"""

    completed = QtCore.pyqtSignal(int)

    def __init__(
        self, articles_data: list[tuple["Article", "PriceStructure", "OSCharges"]], fr
    ) -> None:
        super(QtCore.QThread, self).__init__()

        self.articles_data = articles_data
        self.fixed_rates = fr

    def run(self) -> None:
        """Run task in thread"""

        # Show the status application
        success_count = 0
        for article, ps, oc in self.articles_data:
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

            df = query_fetch_bom_df(article.sap_code, article.size)
            if isinstance(df, pd.DataFrame) and not df.empty:
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
                success_count += 1

        self.completed.emit(success_count)
