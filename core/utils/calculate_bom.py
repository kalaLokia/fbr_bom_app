import math

from typing import TYPE_CHECKING

import pandas as pd


if TYPE_CHECKING:
    from database.database import Article


class BillOfMaterial:
    """Article's bom"""

    def __init__(self, df: pd.DataFrame(), pairs_in_case: int) -> None:
        self.bom_df = df
        self.pairs_in_case = pairs_in_case

        self.updateRexinConsumption()
        self.updateComponentConsumption()
        self.updatePuxConsumption()

        # Calculate and create rate of materials columns
        self.bom_df["rate"] = self.bom_df.apply(
            lambda x: self.calculateRate(x.process_order, x.child_rate, x.child_qty),
            axis=1,
        )
        self.bom_df = self.bom_df.round({"child_qty": 5, "child_rate": 3, "rate": 2})

    @property
    def get_outer_sole(self):
        condition = self.bom_df.child.str.lower().str.startswith("4-pux")
        return tuple(self.bom_df[condition][["child", "child_qty"]].iloc[0])

    @property
    def get_cost_of_materials(self):
        if self.bom_df.empty:
            return 0
        mtypes = ["Synthetic Leather", "Component", "Footwear Sole", "Packing Material"]
        total_sum = self.bom_df[self.bom_df.child_type.isin(mtypes)]["rate"].sum()
        total_sum += 3  # TODO: User specified value ?? Other material cost
        total_sum = math.ceil(total_sum * 100) / 100  # round up to 2 decimal places
        return total_sum

    @property
    def rexine_df(self):
        return self.getTableData("Synthetic Leather")

    @property
    def component_df(self):
        return self.getTableData("Component")

    @property
    def moulding_df(self):
        return self.getTableData("Footwear Sole")

    @property
    def packing_df(self):
        return self.getTableData("Packing Material")

    def updateRexinConsumption(self) -> None:
        """Updates rexine consumption for slitting/folding process"""

        slt_df = self.bom_df[
            (self.bom_df.process_order == 8)
            & (self.bom_df.child_type == "Synthetic Leather")
        ]
        slt_items = slt_df["father"].tolist()
        for i, slt in enumerate(slt_items):
            slt_head_df = self.bom_df[self.bom_df.child == slt]
            if slt_head_df.process_order.iloc[0] < 7:
                length = slt_head_df["child_qty"].iloc[0]
            else:
                fld = slt_head_df.father.iloc[0]
                fld_head_df = self.bom_df[self.bom_df.child == fld]
                length = fld_head_df["child_qty"].iloc[0]

            self.bom_df.loc[slt_df.index.values[i], "child_qty"] *= length

    def updateComponentConsumption(self) -> None:
        """Updates component consumption of folding process"""

        fld_df = self.bom_df[
            (self.bom_df.process_order == 7)
            & (
                (self.bom_df.child_type == "Component")
                | (self.bom_df.child_type == "Other Material")
            )
        ]
        fld_items = fld_df["father"].tolist()
        for i, fld in enumerate(fld_items):
            fld_head_df = self.bom_df[self.bom_df.child == fld]
            if fld_head_df.process_order.iloc[0] < 7:
                length = fld_head_df["child_qty"].iloc[0]
                self.bom_df.loc[fld_df.index.values[i], "child_qty"] *= length

    def updatePuxConsumption(self) -> None:
        """Calculates PUX consumption as per the outer weight"""

        self.bom_df.loc[
            self.bom_df["father"] == self.get_outer_sole[0], "child_qty"
        ] *= self.get_outer_sole[1]

    def calculateRate(self, process, item_rate, qty) -> float:
        rate = item_rate * qty
        if process == 1:
            rate = rate / self.pairs_in_case
        return rate

    def getTableData(self, mtype: str) -> pd.DataFrame:
        """
        Get costsheet table for given material type.

        Args
        -----
            :mtype: -- Material type
        """

        table_data = self.bom_df[self.bom_df.child_type == mtype].filter(
            ["application", "child", "child_item", "child_qty", "child_rate", "rate"]
        )
        table_data = table_data.reset_index(drop=True)
        return table_data
