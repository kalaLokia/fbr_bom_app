"""
Clean and bulk update table bom and article with the data provided.

Works in seperate thread as it is time consuming, that way this 
process will not freeze the main application. All neccessary calculations are
performed using `pandas` to make "bom" and "articles list" tables. 

Mandatory columns:
------------------
bom herirachy:- father, father name, child, child qty, process, process order

materials:- item no, mrp, foreign name, no of pairs, product type, 
            inventory uom, last purchase price

"""

import warnings
import logging

import pandas as pd
from PyQt6 import QtCore
from sqlalchemy.exc import IntegrityError

from database import SQL_T_BOM, SQL_T_ARTICLE
from database.database import engine
from database.sql_db import query_clean_bom_articles


class WorkerThreadBom(QtCore.QThread):
    """
    Create or re-create(if exists) tables "bom" and "article" in database.
    """

    update_progress = QtCore.pyqtSignal(int)
    completed = QtCore.pyqtSignal(bool, str)

    def __init__(self, path_bom, path_items) -> None:
        super(QtCore.QThread, self).__init__()

        self.path_bom = path_bom
        self.path_items = path_items

    def run(self):
        """Perform the task"""
        status, message = self.createBomArticleTable()
        self.completed.emit(status, message)

    def createBomArticleTable(self) -> tuple[bool, str]:
        """
        Clean and bulk update tables "bom" and "article" in database.

        """

        bom_df = pd.DataFrame()
        item_df = pd.DataFrame()

        bom_mandatory_cols = [
            "father",
            "father_name",
            "child",
            "process",
            "process_order",
            "child_qty",
        ]
        items_mandatory_cols = [
            "item_no",
            "foreign_name",
            "mrp",
            "no_of_pairs",
            "inventory_uom",
            "product_type",
            "last_purchase_price",
        ]

        try:
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                item_df = pd.read_excel(self.path_items, engine="openpyxl")
                self.update_progress.emit(13)  # Passing the progress signal
                bom_df = pd.read_excel(self.path_bom, engine="openpyxl")
                self.update_progress.emit(28)  # Passing the progress signal

        except FileNotFoundError:
            return (False, "Files not found in the given directory.")
        except IOError:
            return (
                False,
                "[Permission denied] to read the files. Close the files if they are already opened.",
            )
        except Exception as e:
            return (False, f"[108] Failed to load files,\n({e})")

        if item_df.empty and bom_df.empty:
            return (False, "No records found in the files.")

        self.update_progress.emit(45)  # Passing the progress signal
        # Clean Up dataframes
        bom_df.columns = (
            bom_df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(r"[\./]", "", regex=True)
        )
        item_df.columns = (
            item_df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(r"[\./]", "", regex=True)
        )

        # Checking all required columns exists in the file
        if not all(e in bom_df.columns for e in bom_mandatory_cols):
            return (False, 'Missing required columns in "bom heirarchy" file')

        if not all(e in item_df.columns for e in items_mandatory_cols):
            return (False, 'Missing required columns in "item master data" file')

        self.update_progress.emit(48)  # Passing the progress signal

        # Summing up duplicated rows in bom
        bom_df = bom_df.groupby(by=bom_mandatory_cols[:-1], as_index=False)["child_qty"].sum()
        self.update_progress.emit(49)  # Passing the progress signal


        bom_df["father_name"] = bom_df["father_name"].apply(
            lambda x: x.replace("--", "-").replace("  ", " ").strip().lower()
        )
        bom_df["father"] = bom_df["father"].apply(lambda x: x.strip().upper())
        bom_df["child"] = bom_df["child"].apply(lambda x: x.strip().upper())

        required_cols_bom_db = [
            "father",
            "child",
            "child_qty",
            "process",
            "process_order",
            "child_item",
            "child_uom",
            "child_rate",
            "child_type",
            "application",
        ]
        self.update_progress.emit(51)  # Passing the progress signal

        # Merging item master with bom heirarchy
        bom_df = bom_df.merge(
            item_df[
                ["item_no", "foreign_name", "inventory_uom", "last_purchase_price"]
            ],
            how="left",
            left_on="child",
            right_on="item_no",
        )

        bom_df = bom_df.merge(
            item_df[["item_no", "mrp", "product_type", "no_of_pairs"]],
            how="left",
            left_on="father",
            right_on="item_no",
        )
        bom_df.columns = [self.changeColumnName(name) for name in bom_df.columns.values]
        self.update_progress.emit(58)  # Passing the progress signal

        # Creating article list dataframe before further modification
        art_df = bom_df[bom_df.process_order == 1][
            ["father", "father_name", "product_type", "mrp", "no_of_pairs"]
        ].copy()
        unwanted_cols_bom_db = [
            c for c in bom_df.columns if c not in required_cols_bom_db
        ]
        bom_df.drop(unwanted_cols_bom_db, axis=1, inplace=True, errors="ignore")
        bom_df["child_type"] = bom_df.apply(
            lambda x: self.getMaterialType(x.father, x.child), axis=1
        )
        bom_df["application"] = bom_df.apply(
            lambda x: self.getApplication(x.father, x.process_order), axis=1
        )
        bom_df["child_qty"] = pd.to_numeric(bom_df["child_qty"], errors="coerce")
        bom_df["child_rate"] = pd.to_numeric(bom_df["child_rate"], errors="coerce")

        # Updating and cleaning uo article list dataframe
        art_df.drop_duplicates(inplace=True)
        cond = art_df.father_name.str.contains(
            r"\d[xX]\d"
        ) 
        # For negleting other articles that does not belongs to us
        # Currently skipping this check,
        # & ~art_df.father.str.contains(r"^2-FB-0|^2-FB-S|^2-FB-7")
        art_df = art_df[cond]
        art_df["size_matrix"] = art_df["father_name"].apply(
            lambda x: x.split("-")[5].strip() if len(x.split("-")) > 5 else "0"
        )
        art_df["size_count"] = art_df["size_matrix"].apply(
            lambda x: self.getSizeCount(x)
        )
        art_df.sort_values(
            ["size_count", "father"], inplace=True, ascending=[False, True]
        )
        art_df["brand"] = art_df["father_name"].apply(lambda x: x.split("-")[1].strip())
        art_df["art_no"] = art_df["father_name"].apply(
            lambda x: x.split("-")[2].strip()
        )
        art_df["color"] = art_df["father_name"].apply(lambda x: x.split("-")[3].strip())
        art_df["category"] = art_df["father_name"].apply(
            lambda x: x.split("-")[4].strip()
        )
        art_df["color_code"] = art_df["father"].apply(
            lambda x: x.split("-")[3].strip().lower()
        )
        art_df["category_code"] = art_df["father"].apply(
            lambda x: x.split("-")[4].strip()[0].lower()
        )
        art_df.drop_duplicates(
            subset=["art_no", "color", "category"],
            keep="first",
            inplace=True,
            ignore_index=True,
        )
        art_df["mrp"] = pd.to_numeric(art_df["mrp"], errors="coerce")
        art_df["product_type"] = art_df["product_type"].astype(
            str, copy=False, errors="ignore"
        )
        art_df["product_type"] = art_df["product_type"].apply(
            lambda x: "unknown" if x == "nan" else x.strip().lower()
        )
        art_df["price_structure"] = art_df["brand"].apply(
            lambda x: self.getPriceStructure(x)
        )

        art_df.rename(columns={"father": "sap_code"}, inplace=True)
        art_df.drop(columns=["father_name", "size_count"], inplace=True)
        art_df["article"] = (
            art_df.art_no.str.upper()
            + " "
            + art_df.color.str.title()
            + " "
            + art_df.category.str.title()
        )
        art_df["article_code"] = (
            art_df.art_no.str.upper()
            + "-"
            + art_df.color_code.str.upper()
            + "-"
            + art_df.category_code.str.upper()
        )
        self.update_progress.emit(69)  # Passing the progress signal

        status = query_clean_bom_articles()
        if not status:
            return (
                False,
                "Unable to clear database, check the connection with server.",
            )
        self.update_progress.emit(74)  # Passing the progress signal
        try:
            bom_df.to_sql(
                SQL_T_BOM,
                con=engine,
                if_exists="append",
                index=True,
                index_label="bom_id",
            )
        except IntegrityError as e:
            err = e.args[0].lower()
            if "violation of unique key constraint" in err:
                logging.critical("Duplicate values found while setting up bom!!")
                return (
                    False,
                    "Duplicate values found in the data, cannot proceed further.",
                )
            logging.exception("Database error found while setting up bom!!")
        except Exception as e:
            return (False, f"[Error 108] Server failure #report to me:\n{e}")

        self.update_progress.emit(88)  # Passing the progress signal
        try:
            art_df.to_sql(
                SQL_T_ARTICLE,
                con=engine,
                if_exists="append",
                index=False,
            )
        except IntegrityError as e:
            err = e.args[0].lower()
            if "violation of primary key constraint" in err:
                logging.critical("Duplicate values found while setting up article list!!")
                return (
                    False,
                    "Duplicate values found in the data, cannot proceed further.",
                )
            logging.exception("Database error found while setting up article list!!")
        except Exception as e:
            return (False, f"[Error 108] Server failure #report to me:\n{e}")

        self.update_progress.emit(100)  # Passing the progress signal
        return (True, "Successfully updated the database.")

    @staticmethod
    def changeColumnName(name) -> str:
        """For changing column names of the dataframe"""
        return {
            "foreign_name": "child_item",
            "inventory_uom": "child_uom",
            "last_purchase_price": "child_rate",
        }.get(name, name)

    @staticmethod
    def getMaterialType(head: str, tail: str) -> str:
        item = tail[2:4].lower()
        head_item = "".join(head.split("-")[1:2]).lower()

        material_types = {
            "nl": "Synthetic Leather",
            "co": "Component",
            "pu": "PU Mix",
            "km": "Component",
        }
        default_material_types = {
            "fb": "Packing Material",
            "mpu": "Footwear Sole",
            "pux": "Footwear Sole",
        }
        try:
            value = int(tail[0])
            if value > 4 or tail[:5].lower() == "4-pux" or item == "km":
                default_type = default_material_types.get(head_item, "Other Material")
                return material_types.get(item, default_type)
            else:
                return item
        except:
            return "Unknown"

    @staticmethod
    def getApplication(head, process) -> str:
        value = "".join(head.split("-")[1:2])

        if value.lower() == "fb":
            if process == 1:
                return "MC"
            elif process == 2:
                return "SC"
            else:
                return "NA"
        else:
            return value

    @staticmethod
    def getPriceStructure(brand: str) -> str:
        if brand in ["debongo", "vkc debongo dx", "kapers", "lkapers"]:
            return "D"
        elif brand in ["stile"]:
            return "S"
        else:
            return "P"

    @staticmethod
    def getSizeCount(size_matrix):
        """Total sizes in the given size matrix"""
        try:
            small, big = size_matrix.split("x")
            count = int(big) - int(small) + 1
        except ValueError:
            count = -1
        except:
            count = 0
        return count
