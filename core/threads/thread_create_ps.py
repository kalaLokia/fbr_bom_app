import warnings

import pandas as pd
from PyQt6 import QtCore
from sqlalchemy.exc import IntegrityError

from database import SQL_T_PRICE_STRUCTURE
from database.database import engine
from database.sql_db import query_clean_price_structure


class WorkerThreadPriceStructure(QtCore.QThread):
    """
    Clean and bulk update table price structure in database.

    """

    completed = QtCore.pyqtSignal(bool, str)

    def __init__(self, path_to_file) -> None:
        super(QtCore.QThread, self).__init__()

        self.path_to_file = path_to_file

    def run(self):
        """Perform the task"""
        status, message = self.createPriceStructureTable()
        self.completed.emit(status, message)

    def createPriceStructureTable(self):
        """
        Create or re-create(if exists) table "price_structure" in database.

        Excel file with name "Price Structure" required with columns:
            -  price_structure
            -  mrp
            -  basic

        """

        df = pd.DataFrame()
        ps_required_cols = ["price_structure", "mrp", "basic"]

        try:
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                df = pd.read_excel(self.path_to_file, engine="openpyxl")
                df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
                if not all(e in df.columns for e in ps_required_cols):
                    raise ValueError("Missing required columns in the record.")
                df["mrp"].astype(float)
                df["basic"].astype(float)
                df["price_structure"] = df["price_structure"].str.upper()
                df.fillna(0)

                status = query_clean_price_structure()
                if not status:
                    return (
                        False,
                        "Unable to clear database, check the connection with server.",
                    )

                df.to_sql(
                    SQL_T_PRICE_STRUCTURE,
                    con=engine,
                    if_exists="append",
                    index=False,
                )

        except FileNotFoundError:
            return (False, "Files not found in the given directory.")
        except IOError:
            return (
                False,
                "[Permission denied] to read the files. Close the files if they are already opened.",
            )
        except ValueError:
            return (
                False,
                'Missing required columns in the record, expecting "price_structure" | "mrp" | "basic"',
            )
        except IntegrityError as e:
            err = e.args[0].lower()
            if "violation of primary key constraint" in err:
                return (
                    False,
                    "Duplicate values found in the data, cannot update data.",
                )
        except Exception as e:
            return (False, f"[108] Failed to load files,\n({e})")

        return (True, "Successfully updated the database with new Price Structure.")
