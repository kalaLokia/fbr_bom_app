import warnings

import pandas as pd
from PyQt6 import QtCore
from sqlalchemy.exc import IntegrityError

from database import SQL_T_CHARGES
from database.database import engine
from database.sql_db import query_clean_os_charges


class WorkerThreadOsCharges(QtCore.QThread):
    """
    Clean and bulk update table OSCharges in database.

    """

    completed = QtCore.pyqtSignal(bool, str)

    def __init__(self, path_to_file) -> None:
        super(QtCore.QThread, self).__init__()

        self.path_to_file = path_to_file

    def run(self):
        """Perform the task"""
        status, message = self.createOsChargesTable()
        self.completed.emit(status, message)

    def createOsChargesTable(self):
        """
        Create or re-create(if exists) table "os_charges" in database.

        Excel file with name "OS Charges" required with columns:
            -  article
            -  stitching
            -  printing

        """

        df = pd.DataFrame()
        os_charges_req_cols = ["article", "stitching", "printing"]

        try:
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                df = pd.read_excel(self.path_to_file, engine="openpyxl")
                df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
                if not all(e in df.columns for e in os_charges_req_cols):
                    raise ValueError("Missing required columns in the record.")

                df["article"] = df["article"].str.upper()
                df["stitching"].astype(float)
                df["printing"].astype(float)
                df.fillna(0)

                status = query_clean_os_charges()
                if not status:
                    return (
                        False,
                        "Unable to clear database, check the connection with server.",
                    )

                df.to_sql(SQL_T_CHARGES, con=engine, if_exists="append", index=False, chunksize=1000)

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
                'Missing required columns in the record, expecting "article" | "stitching" | "printing"',
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

        return (True, "Successfully updated the database with new OS Charges.")
