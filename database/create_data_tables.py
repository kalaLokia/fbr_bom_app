"""
Creates or replaces(if exists) tables "bom" and "articles" into the database.

"""

import warnings

import pandas as pd
from .database import engine
from .sql_db import (
    query_clean_os_charges,
    query_clean_price_structure,
)


from . import (
    SQL_T_PRICE_STRUCTURE,
    SQL_T_CHARGES,
)


def createOsChargesTable():
    """
    Create or re-create(if exists) table "os_charges" in database.

    Excel file with name "OS Charges" required with columns:
        -  article
        -  stitching
        -  printing

    """

    dir = "data/OS Charges.xlsx"
    df = pd.DataFrame()

    try:
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            df = pd.read_excel(dir, engine="openpyxl")
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            df["article"] = df["article"].str.upper()
            df["stitching"].astype(float)
            df["printing"].astype(float)
            df.fillna(0)

            query_clean_os_charges()

            df.to_sql(SQL_T_CHARGES, con=engine, if_exists="append", index=False)

    except FileNotFoundError:
        print("File not found")
        return (False, "File not found.")
    except IOError:
        print("No access to read file")
        return (False, "No access to the file.")
    except Exception as e:
        print(e)
        return (False, "Failed (108)")

    return (True, "Success")


def createPriceStructureTable():
    """
    Create or re-create(if exists) table "price_structure" in database.

    Excel file with name "Price Structure" required with columns:
        -  price_structure
        -  mrp
        -  basic

    """

    dir = "data/Price Structure.xlsx"
    df = pd.DataFrame()

    try:
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            df = pd.read_excel(dir, engine="openpyxl")
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            df["mrp"].astype(float)
            df["basic"].astype(float)
            df["price_structure"] = df["price_structure"].str.upper()
            df.fillna(0)

            query_clean_price_structure()

            df.to_sql(
                SQL_T_PRICE_STRUCTURE,
                con=engine,
                if_exists="append",
                index=False,
            )

    except FileNotFoundError:
        print("File not found")
        return (False, "File not found.")
    except IOError:
        print("No access to read file")
        return (False, "No access to the file.")
    except Exception as e:
        print("Error\n %s" % e)
        return (False, "Failed (108)")

    return (True, "Success")
