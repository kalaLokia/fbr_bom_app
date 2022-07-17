"""
Excel reporting.

Yep, I know it is little mess.. I don't wanna spend much time on this. ;')

"""

from typing import TYPE_CHECKING
from io import BytesIO

import pandas as pd

from settings import EXPORT_DIR, SBU_NAME


if TYPE_CHECKING:
    from database.database import Article, OSCharges


class ExcelReporting:
    def __init__(
        self,
        article: "Article",
        os_charges: "OSCharges",
        basic_rate: float,
        fixed_rates,
        nl_df,
        co_df,
        pu_df,
        pm_df,
    ) -> None:
        self.article = article
        self.os_charges = os_charges
        self.basic_rate = basic_rate
        self.nl_df = nl_df
        self.co_df = co_df
        self.pu_df = pu_df
        self.pm_df = pm_df
        self.workbook = None
        self.worksheet = None

        self.nl_start_row = 7
        self.co_start_row = 2
        self.pu_start_row = 2 + 5
        self.pm_start_row = 2 + 6
        self.pm_end_row = 2
        self.row_total_cost = 0
        self.row_total_other_expense = 0
        self.last_row = 2

        self.expenses_overheads = (
            ("Nothing", 0)
            if not fixed_rates
            else [
                (rate.name, rate.value)
                for rate in fixed_rates
                if rate.rate_type.upper() == "OH"
            ]
        )
        self.selling_and_distr = (
            0
            if not fixed_rates
            else float(
                [
                    rate.value
                    for rate in fixed_rates
                    if rate.name.lower() == "selling and distribution"
                ][-1]
            )
            / 100
        )
        self.royality = (
            0
            if not fixed_rates
            else float(
                [rate.value for rate in fixed_rates if rate.name.lower() == "royality"][
                    -1
                ]
            )
            / 100
        )
        self.sales_return = (
            0
            if not fixed_rates
            else float(
                [
                    rate.value
                    for rate in fixed_rates
                    if rate.name.lower() == "sales return"
                ][-1]
            )
            / 100
        )

    @property
    def get_nl_rows(self):
        return self.nl_df.shape[0]

    @property
    def get_co_rows(self):
        return self.co_df.shape[0]

    @property
    def get_pu_rows(self):
        return self.pu_df.shape[0]

    @property
    def get_pm_rows(self):
        return self.pm_df.shape[0]

    @property
    def total_rows_on_sheet(self):
        content_rows = (
            self.get_nl_rows + self.get_co_rows + self.get_pu_rows + self.get_pm_rows
        )
        constant_rows = 10
        return content_rows + constant_rows

    def allocateRows(self):
        self.co_start_row += self.get_nl_rows + self.nl_start_row
        self.pu_start_row += self.get_co_rows + self.co_start_row
        self.pm_start_row += self.get_pu_rows + self.pu_start_row
        self.pm_end_row += self.get_pm_rows + self.pm_start_row
        self.last_row += self.pm_end_row + 2

    def writeConstantFields(self):
        # Workbook formatting

        fmt_artinfo1 = self.workbook.add_format(
            {"valign": "vcenter", "align": "center", "bg_color": "#ffe6d9"}
        )
        fmt_artinfo2 = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "center",
                "font_name": "Calibri Light",
                "font_size": 12,
                "bold": True,
                "bg_color": "#ffe6d9",
            }
        )
        fmt_costsheet = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "center",
                "font_name": "Calibri Light",
                "font_size": 14,
                "bold": True,
            }
        )
        fmt_branch = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "center",
                "font_name": "Georgia",
                "font_size": 14,
                "bold": True,
                "underline": True,
            }
        )
        fmt_textC = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "center",
                "font_name": "Calibri Light",
                "font_size": 11,
            }
        )
        fmt_textL = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "left",
                "font_name": "Calibri Light",
                "font_size": 11,
            }
        )
        fmt_textR = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "right",
                "font_name": "Calibri Light",
                "font_size": 11,
            }
        )
        fmt_textBL = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "left",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bold": True,
            }
        )
        fmt_textBR = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "right",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bold": True,
            }
        )
        fmt_textBC = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "center",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bold": True,
            }
        )
        fmt_textBC_grey = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "center",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bold": True,
                "bg_color": "#c7c7c7",
            }
        )
        fmt_darkgrey = self.workbook.add_format({"bg_color": "#757575"})
        fmt_align_center = self.workbook.add_format({"align": "center"})

        # Adjust column width
        self.worksheet.set_column(1, 1, 19, fmt_align_center)
        self.worksheet.set_column(2, 2, 16, fmt_align_center)
        self.worksheet.set_column(3, 3, 75)
        self.worksheet.set_column(4, 6, 12.2)
        self.worksheet.set_row(1, 18)
        self.worksheet.set_row(2, 18)
        self.worksheet.set_row(3, 18)
        self.worksheet.set_row(4, 18)

        # Write Headers
        self.worksheet.write(1, 1, "Brand", fmt_artinfo1)
        self.worksheet.write(2, 1, "Article", fmt_artinfo1)
        self.worksheet.write(3, 1, "Color", fmt_artinfo1)
        self.worksheet.write(4, 1, "Category", fmt_artinfo1)
        self.worksheet.merge_range("D2:D3", SBU_NAME, fmt_branch)
        self.worksheet.write("D4", "COST SHEET", fmt_costsheet)
        self.worksheet.write(2, 5, "Size", fmt_textC)
        self.worksheet.write(3, 4, "PER PAIR", fmt_textC)
        self.worksheet.write(3, 5, "PER UOM", fmt_textC)
        self.worksheet.write(3, 6, "PER PAIR", fmt_textC)

        # Title
        self.worksheet.write(6, 1, "APPLICATION", fmt_textC)
        self.worksheet.write(6, 2, "ITEM CODE", fmt_textC)
        self.worksheet.write(6, 3, "MATERIAL", fmt_textC)
        self.worksheet.write(6, 4, "Consumption", fmt_textC)
        self.worksheet.write(6, 5, "Landed rate", fmt_textC)
        self.worksheet.write(6, 6, "RATE /pair", fmt_textC)
        # Break Line
        for c in range(1, 7):
            self.worksheet.write(5, c, None, fmt_darkgrey)

        # Write Article Info
        self.worksheet.write(1, 2, self.article.brand.upper(), fmt_artinfo2)
        self.worksheet.write(2, 2, self.article.art_no.upper(), fmt_artinfo2)
        self.worksheet.write(3, 2, self.article.color.upper(), fmt_artinfo2)
        self.worksheet.write(4, 2, self.article.category.upper(), fmt_artinfo2)
        self.worksheet.write(2, 6, self.article.size, fmt_textC)

        # __________CONTENTS____________
        # Material 1
        self.worksheet.write(self.nl_start_row, 1, "Synthetic Leather", fmt_textBC_grey)
        for c in range(2, 7):
            self.worksheet.write(self.nl_start_row, c, None, fmt_textBC_grey)
        # Material 2
        self.worksheet.write(self.co_start_row, 1, "Component", fmt_textBC_grey)
        for c in range(2, 7):
            self.worksheet.write(self.co_start_row, c, None, fmt_textBC_grey)
        self.worksheet.write(self.pu_start_row - 3, 3, "STITCHING CHARGES", fmt_textBR)
        self.worksheet.write(
            self.pu_start_row - 2, 3, "PRINTING & EMBOSSING", fmt_textBR
        )
        self.worksheet.write(
            self.pu_start_row - 1, 3, "Cost of Footwear Upper", fmt_textBL
        )

        self.worksheet.write(
            self.pu_start_row - 3, 6, self.os_charges.stitch_rate, fmt_textR
        )  # stitch
        self.worksheet.write(
            self.pu_start_row - 2, 6, self.os_charges.print_rate, fmt_textR
        )  # print

        cost_upper = f"=SUM($G${self.nl_start_row + 2}:$G${self.pu_start_row - 1})"
        self.worksheet.write_formula(self.pu_start_row - 1, 6, cost_upper, fmt_textBR)
        # Material 3
        self.worksheet.write(self.pu_start_row, 1, "Footwear Sole", fmt_textBC_grey)
        for c in range(2, 7):
            self.worksheet.write(self.pu_start_row, c, None, fmt_textBC_grey)

        self.worksheet.write(self.pm_start_row - 4, 3, "OTHER CHEMICAL", fmt_textBR)
        self.worksheet.write(self.pm_start_row - 4, 6, 3, fmt_textR)
        self.worksheet.write(
            self.pm_start_row - 3, 3, "NORMAL WASTAGE @ 5%", fmt_textBR
        )
        self.worksheet.write(
            self.pm_start_row - 1, 3, "Cost of Footwear Sole", fmt_textBL
        )

        cost_sole = f"=SUM($G${self.pu_start_row + 2}:$G${self.pm_start_row - 2})"
        self.worksheet.write(self.pm_start_row - 1, 6, cost_sole, fmt_textBR)

        # Material 4
        self.worksheet.write(self.pm_start_row, 1, "Packing Material", fmt_textBC_grey)

        self.worksheet.write(
            self.pm_start_row, 2, self.article.pairs_in_case, fmt_textBC_grey
        )
        for c in range(3, 7):
            self.worksheet.write(self.pm_start_row, c, None, fmt_textBC_grey)

        self.worksheet.write(self.pm_end_row, 3, "Cost of Packing Material", fmt_textBL)
        cost_packing = f"=SUM($G${self.pm_start_row + 2}:$G${self.pm_end_row - 1})"
        self.worksheet.write(self.pm_end_row, 6, cost_packing, fmt_textBR)
        total_cost_upper = "=SUM($G${0}, $G${1}, $G${2})".format(
            self.pu_start_row, self.pm_start_row, self.pm_end_row + 1
        )
        for c in range(1, 7):
            self.worksheet.write(self.pm_end_row + 2, c, None, fmt_textBC_grey)
        # TOTAL COST OF MATERIALS
        self.worksheet.write(self.last_row, 3, "TOTAL COST OF MATERIALS", fmt_textBL)
        self.worksheet.write_formula(self.last_row, 6, total_cost_upper, fmt_textBR)
        self.row_total_cost = self.last_row + 1
        self.last_row += 2

        self.constRateDetails(fmt_textL, fmt_textR, fmt_textBR)
        self.footer(fmt_textBL, fmt_textBC, fmt_textL, fmt_textR)

    def constRateDetails(self, fmt_L, fmt_R, fmt_B):
        start = self.last_row + 1
        for i, (name, value) in enumerate(self.expenses_overheads):
            item = "{0}-{1}".format(i + 1, name.title())
            self.worksheet.write(self.last_row, 3, item, fmt_L)
            self.worksheet.write(self.last_row, 6, value, fmt_R)
            self.last_row += 1
        end = self.last_row
        self.row_total_other_expense = self.last_row + 3
        self.worksheet.write_formula(
            self.row_total_other_expense - 1, 6, f"=SUM($G${start}:$G${end})", fmt_B
        )
        self.last_row += 4

    def footer(self, fmt_B, fmt_BC, fmt_L, fmt_R):
        formula_total_cost_of_prod = "=SUM($G${0}, $G${1})".format(
            self.row_total_cost, self.row_total_other_expense
        )

        reddish = "#ffd1b5"
        orange = "#ffad33"

        fmt_percent = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "center",
                "font_name": "Calibri Light",
                "font_size": 11,
                "num_format": "0.00%",
            }
        )

        fmt_orangeBL = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "left",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bold": True,
                "bg_color": orange,
            }
        )
        fmt_orangeBR = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "right",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bold": True,
                "bg_color": orange,
            }
        )

        fmt_reddishL = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "left",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bg_color": reddish,
            }
        )
        fmt_reddishR = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "right",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bg_color": reddish,
            }
        )
        fmt_blueBR = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "right",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bg_color": "#99ffec",
                "bold": True,
            }
        )
        fmt_reddishBL = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "left",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bg_color": reddish,
                "bold": True,
            }
        )
        fmt_reddishPercent = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "center",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bg_color": reddish,
                "bold": True,
                "num_format": "0.00%",
            }
        )
        fmt_yellowR = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "right",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bg_color": "#FFFF00",
            }
        )
        fmt_BR = self.workbook.add_format(
            {
                "valign": "vcenter",
                "align": "right",
                "font_name": "Calibri Light",
                "font_size": 11,
                "bold": True,
            }
        )
        row_basic_price = self.last_row + 10
        sell_distr_F = f"=$E${self.last_row + 3} * $G${row_basic_price}"
        royalty_F = f"=$E${self.last_row + 4} * $G${row_basic_price}"
        goods_sold_F = f"=SUM($G${self.last_row + 1}, $G${self.last_row + 3}, $G${self.last_row + 4})"
        sale_return_F = f"=$E${self.last_row + 6} * $G${self.last_row + 5}"
        total_F = f"=SUM($G${self.last_row + 5}, $G${self.last_row + 6})"
        net_margin_F = f"=IFERROR($G${self.last_row + 8} / $G${row_basic_price}," ")"
        net_margin_F2 = f"=$G${row_basic_price} - $G${self.last_row + 7}"
        gross_margin_F = f'=IFERROR(($G${row_basic_price}-($G${self.last_row + 7}-$G${self.row_total_other_expense}))/$G${row_basic_price},"")'
        gross_margin_F2 = f'=IFERROR($E${self.last_row + 9} * $G${row_basic_price}," ")'
        data = [
            [
                "Cost of Production",
                "",
                formula_total_cost_of_prod,
                [fmt_orangeBL, fmt_orangeBR, fmt_orangeBR],
            ],
            ["", "", "", [fmt_L, fmt_L, fmt_L]],
            [
                "Selling and Distribution",
                self.selling_and_distr,
                sell_distr_F,
                [fmt_L, fmt_percent, fmt_R],
            ],
            ["Royalty", self.royality, royalty_F, [fmt_L, fmt_percent, fmt_R]],
            [
                "Cost of Goods Sold",
                "",
                goods_sold_F,
                [fmt_reddishL, fmt_reddishL, fmt_reddishR],
            ],
            [
                "Sales Return",
                self.sales_return,
                sale_return_F,
                [fmt_L, fmt_percent, fmt_R],
            ],
            ["TOTAL", "", total_F, [fmt_B, fmt_BC, fmt_R]],
            [
                "NET MARGIN",
                net_margin_F,
                net_margin_F2,
                [fmt_reddishBL, fmt_reddishPercent, fmt_blueBR],
            ],
            [
                "GROSS MARGIN",
                gross_margin_F,
                gross_margin_F2,
                [fmt_reddishBL, fmt_reddishPercent, fmt_blueBR],
            ],
            ["BASIC/FACTORY PRICE", "", 0, [fmt_L, fmt_L, fmt_yellowR]],
            ["MAXIMUM RETAIL PRICE", "", 0, [fmt_L, fmt_L, fmt_yellowR]],
        ]
        start = self.last_row + 1

        for item in data:
            self.worksheet.write(self.last_row, 3, item[0], item[3][0])
            self.worksheet.write(self.last_row, 4, item[1], item[3][1])
            self.worksheet.write(self.last_row, 6, item[2], item[3][2])
            self.worksheet.write(self.last_row, 5, "", item[3][0])
            self.last_row += 1
        end = self.last_row
        self.worksheet.write(end - 2, 6, self.basic_rate, fmt_BR)  # basic price
        self.worksheet.write(end - 1, 6, self.article.mrp, fmt_BR)  # mrp
        self.worksheet.merge_range(f"B{start}:C{end}", "")

    def generateTable(self, filename: str = None, filepath: str = None):
        """
        Generate report file.

        Args:
            :filename: - Filename with full path
            :filepath: - Full path to file saving directory

        Only one of the argument is considered, priority to `filename`

        """

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        self.workbook = writer.book
        self.allocateRows()

        self.nl_df.to_excel(
            writer,
            sheet_name="costsheet",
            startrow=self.nl_start_row + 1,
            startcol=1,
            header=False,
            index=False,
        )
        self.co_df.to_excel(
            writer,
            sheet_name="costsheet",
            startrow=self.co_start_row + 1,
            startcol=1,
            header=False,
            index=False,
        )
        self.pu_df.to_excel(
            writer,
            sheet_name="costsheet",
            startrow=self.pu_start_row + 1,
            startcol=1,
            header=False,
            index=False,
        )
        self.pm_df.to_excel(
            writer,
            sheet_name="costsheet",
            startrow=self.pm_start_row + 1,
            startcol=1,
            header=False,
            index=False,
        )

        for ws in self.workbook.worksheets():
            self.worksheet = ws

        self.writeConstantFields()

        # Set borders to all cells
        fmt_border = self.workbook.add_format({"border": 1})
        self.worksheet.conditional_format(
            f"B2:G{self.last_row}",
            {"type": "no_errors", "format": fmt_border},
        )
        fmt_rate = self.workbook.add_format(
            {"num_format": '_ * #,##0.00_ ;_ * -#,##0.00_ ;_ * " - "??_ ;_ @_ '}
        )
        self.worksheet.conditional_format(
            f"G9:G{self.last_row}",
            {"type": "no_blanks", "format": fmt_rate},
        )
        writer.save()

        if not filename:
            filename = self.article.get_filename
            if not filepath:
                filename = EXPORT_DIR + "/" + filename
            else:
                filename = filepath + "/" + filename

        status = self.write_bytes_to_xlsx(output, filename)
        return status

    def write_bytes_to_xlsx(self, excel, filename):
        try:
            with open(filename, "wb+") as f:
                f.write(excel.getvalue())
        except PermissionError:
            return {
                "status": "ERR",
                "message": f"Permission denied. Close the file ({self.article.get_filename}) if it is already being used.",
            }
        except Exception as e:
            return {
                "status": "ERR",
                "message": f"Uncaught error:\n {e}",
            }

        return {
            "status": "CREATED",
            "message": f'Successfully exported costsheet for "{self.article.article}".',
        }
