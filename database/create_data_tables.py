"""
Creates or replaces(if exists) tables "bom" and "articles" into the database.

"""

import warnings

import pandas as pd
import sqlalchemy as sa
from .database import engine
from .sql_db import (
    query_clean_os_charges,
    query_clean_bom_articles,
    query_clean_price_structure,
)


from . import SQL_T_BOM, SQL_T_ARTICLE, SQL_CONN, SQL_T_PRICE_STRUCTURE, SQL_T_CHARGES


def createBomArticleTable():
    """
    Create or re-create(if exists) tables "bom" and "article" in database.

    Excel file with name "Bom Herirachy final" required with columns:
        -  father
        -  father name
        -  child
        -  child qty
        -  process
        -  process order

    Excel file with name "materials" required with columns:
        -  item no
        -  foreign name
        -  no of pairs
        -  inventory uom

    """

    bom_df = pd.DataFrame()
    item_df = pd.DataFrame()
    bom_dir = "data/Bom Hierarchy final.xlsx"
    item_dir = "data/materials.xlsx"

    try:
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            bom_df = pd.read_excel(bom_dir, engine="openpyxl")
            item_df = pd.read_excel(item_dir, engine="openpyxl")

    except FileNotFoundError:
        print("File not found")
        return (False, "File not found.")
    except IOError:
        print("No access to read file")
        return (False, "No access to the file.")
    except Exception as e:
        print(e)
        return (False, "Failed (108)")

    if item_df.empty and bom_df.empty:
        print("No data found")
        return (False, "Empty files")

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

    # Merging item master with bom heirarchy
    bom_df = bom_df.merge(
        item_df[["item_no", "foreign_name", "inventory_uom", "last_purchase_price"]],
        how="left",
        left_on="child",
        right_on="item_no",
    )

    bom_df = bom_df.merge(
        item_df[["item_no", "item_mrp", "product_type", "no_of_pairs"]],
        how="left",
        left_on="father",
        right_on="item_no",
    )
    bom_df.columns = [changeColumnName(name) for name in bom_df.columns.values]
    # Creating article list dataframe before further modification
    art_df = bom_df[bom_df.process_order == 1][
        ["father", "father_name", "product_type", "mrp", "no_of_pairs"]
    ].copy()
    unwanted_cols_bom_db = [c for c in bom_df.columns if c not in required_cols_bom_db]
    bom_df.drop(unwanted_cols_bom_db, axis=1, inplace=True, errors="ignore")
    bom_df["child_type"] = bom_df.apply(
        lambda x: getMaterialType(x.father, x.child), axis=1
    )
    bom_df["application"] = bom_df.apply(
        lambda x: getApplication(x.father, x.process_order), axis=1
    )
    bom_df["child_qty"] = pd.to_numeric(bom_df["child_qty"], errors="coerce")
    bom_df["child_rate"] = pd.to_numeric(bom_df["child_rate"], errors="coerce")

    # Updating and cleaning uo article list dataframe
    art_df.drop_duplicates(inplace=True)
    cond = art_df.father_name.str.contains(r"\d[xX]\d") & ~art_df.father.str.contains(
        r"^2-FB-0|^2-FB-S|^2-FB-7"
    )
    art_df = art_df[cond]
    art_df["size_matrix"] = art_df["father_name"].apply(
        lambda x: x.split("-")[5].strip()
    )
    art_df["size_count"] = art_df["size_matrix"].apply(lambda x: getSizeCount(x))
    art_df.sort_values("size_count", inplace=True, ascending=False)
    art_df["brand"] = art_df["father_name"].apply(lambda x: x.split("-")[1].strip())
    art_df["art_no"] = art_df["father_name"].apply(lambda x: x.split("-")[2].strip())
    art_df["color"] = art_df["father_name"].apply(lambda x: x.split("-")[3].strip())
    art_df["category"] = art_df["father_name"].apply(lambda x: x.split("-")[4].strip())
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
    art_df["price_structure"] = art_df["brand"].apply(lambda x: getPriceStructure(x))

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

    query_clean_bom_articles()

    bom_df.to_sql(
        SQL_T_BOM,
        con=engine,
        if_exists="append",
        index=True,
        index_label="index",
    )
    art_df.to_sql(
        SQL_T_ARTICLE,
        con=engine,
        if_exists="append",
        index=False,
    )

    return (True, "Success")


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


############################################################
# Supportive methods for the database modification process #


def changeColumnName(name) -> str:
    """For changing column names of the dataframe"""
    return {
        "foreign_name": "child_item",
        "inventory_uom": "child_uom",
        "item_mrp": "mrp",
        "last_purchase_price": "child_rate",
    }.get(name, name)


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


def getPriceStructure(brand: str) -> str:
    if brand in ["debongo", "vkc debongo dx", "kapers", "lkapers"]:
        return "D"
    elif brand in ["stile"]:
        return "S"
    else:
        return "P"


def getSizeCount(size_matrix):
    """Total sizes in the given size matrix"""

    small, big = size_matrix.split("x")
    try:
        count = int(big) - int(small) + 1
    except:
        count = 0
    return count
