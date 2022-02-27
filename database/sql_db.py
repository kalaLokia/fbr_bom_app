"""
SQL queries execution

"""

from typing import Union
import sqlalchemy as sa
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from .database import Bom, Article, OSCharges, PriceStructure, engine, FixedRates
from . import SQL_DB_NAME, SQL_T_BOM


Session = sessionmaker(bind=engine)


def query_clean_os_charges():
    """Clean all data from table 'tbl_os_charges'"""
    with Session() as s:
        s.query(OSCharges).delete()
        s.commit()


def query_clean_price_structure():
    """Clean all data from table 'tbl_price_structure'"""
    with Session() as s:
        s.query(PriceStructure).delete()
        s.commit()


def query_clean_bom_articles():
    """Clean all data from tables 'tbl_bom' and  'tbl_article'"""
    with Session() as s:
        s.query(Bom).delete()
        s.query(Article).delete()
        s.commit()


def query_fetch_fixed_rates():
    """Fetch all rows in FixedRates table"""

    result = None
    with Session() as s:
        result = s.query(FixedRates).all()
    return result


def query_list_articles_all():
    """List all articles"""
    result = None
    with Session() as s:
        result = (
            s.query(
                Article,
                PriceStructure,
                OSCharges,
            )
            .select_from(Article)
            .join(
                PriceStructure,
                (PriceStructure.ps_code == Article.ps_code)
                & (PriceStructure.mrp == Article.mrp),
                isouter=True,
                full=False,
            )
            .join(
                OSCharges,
                OSCharges.article == Article.article_code,
                isouter=True,
                full=False,
            )
            .order_by(Article.art_no, Article.category, Article.color)
            .all()
        )
    return result


def query_fetch_all_os_charges() -> list[OSCharges]:
    """Fetch all os charges data"""
    result = None
    with Session() as s:
        result = s.query(OSCharges).order_by(OSCharges.article).all()
    return result


def query_fetch_all_price_structure() -> list[PriceStructure]:
    """Fetch all price structure data"""
    result = None
    with Session() as s:
        result = (
            s.query(PriceStructure)
            .order_by(PriceStructure.ps_code, PriceStructure.mrp)
            .all()
        )
    return result


def query_fetch_bom_df(search_key: str, size: int) -> Union[pd.DataFrame, None]:
    """Fetch and return bom dataframe of the article

    Runs recursive query on database to fetch the bom.

    """
    # Recursive query
    raw_query = f"""WITH cte AS (
        SELECT *
        FROM [{SQL_DB_NAME}].[dbo].[{SQL_T_BOM}]
        WHERE father = '{search_key}'
        UNION ALL
        SELECT p.*
        FROM [{SQL_DB_NAME}].[dbo].[{SQL_T_BOM}] p
        INNER JOIN cte ON cte.child = p.father
        WHERE
        cte.child Like '%{size}' OR cte.child Like '%l' OR cte.child Like '%g'
        OR cte.child Like '%x' OR cte.child Like '%b' OR cte.child Like '%r' 
        OR cte.child Like '%k' OR cte.child Like '%c' 
        OR cte.child Like '4-pux%' OR cte.child Like '4-cca-ang%'
    )
    SELECT * FROM cte
    ORDER BY cte.process_order, cte.father, cte.child
    option (maxrecursion 100);"""

    df = None
    try:
        df = pd.read_sql(raw_query, engine)
    except Exception as e:
        print(e)
        df = None

    return df


def query_setup_charges_table():
    """Setup fixed rates table with initial values.

    Note:-
        OH - Overheads
        OC - Other Charges
        SR - Sales Return
    """

    initial_values = [
        FixedRates(
            name="Wastage and Benefits", value=9.72, value_fmt="rate", rate_type="OH"
        ),
        FixedRates(
            name="Salaries and Emoluments", value=0.79, value_fmt="rate", rate_type="OH"
        ),
        FixedRates(
            name="Other Factory Overheads", value=1.73, value_fmt="rate", rate_type="OH"
        ),
        FixedRates(name="Admin Expenses", value=1.37, value_fmt="rate", rate_type="OH"),
        FixedRates(
            name="Interest and Bank Charges",
            value=0.02,
            value_fmt="rate",
            rate_type="OH",
        ),
        FixedRates(name="Depreciation", value=4.35, value_fmt="rate", rate_type="OH"),
        FixedRates(name="Other Expenses", value=0.0, value_fmt="rate", rate_type="OH"),
        FixedRates(name="Finance Costs", value=1.06, value_fmt="rate", rate_type="OH"),
        FixedRates(
            name="Selling and Distribution",
            value=16.75,
            value_fmt="percent",
            rate_type="OC",
        ),
        FixedRates(name="Royality", value=0.5, value_fmt="percent", rate_type="OC"),
        FixedRates(name="Sales Return", value=1, value_fmt="percent", rate_type="SR"),
    ]

    try:
        with Session() as s:
            s.bulk_save_objects(initial_values)
            s.commit()
    except Exception as e:
        print(e)


# Create, Update, Delete
def query_add_os_charge(obj: OSCharges) -> tuple[bool, str]:
    response = (False, "Unknown Error")
    try:
        with Session() as s:
            try:
                s.add(obj)
                s.commit()
                response = (True, f'Os Charges for "{obj.article}" saved successfully.')
            except Exception as e:
                s.rollback()
                return (False, f"Execution failed.\n{e}")
    except:
        return (False, "Cannot establish connection with server.")

    return response


def query_update_os_charge(obj: OSCharges) -> tuple[bool, str]:
    response = (False, "Unknown Error")
    try:
        with Session() as s:
            try:
                update_obj: OSCharges = (
                    s.query(OSCharges).filter(OSCharges.article == obj.article).one()
                )
                update_obj.print_rate = obj.printing
                update_obj.stitch_rate = obj.stitching
                s.commit()
                response = (
                    True,
                    f'Os Charges for "{obj.article}" updated successfully.',
                )
            except Exception as e:
                s.rollback()
                return (False, f"Execution failed.\n{e}")
    except:
        return (False, "Cannot establish connection with server.")

    return response


def query_delete_os_charges(items: list[str]) -> tuple[bool, str]:
    response = (False, "Unknown Error")
    try:
        with Session() as s:
            try:
                query = s.query(OSCharges).filter(OSCharges.article.in_(items))
                query.delete(synchronize_session=False)
                s.commit()
                response = (
                    True,
                    f"Successfully removed {len(items)} items from database.",
                )
            except Exception as e:
                s.rollback()
                return (False, f"Execution failed.\n{e}")
    except:
        return (False, "Cannot establish connection with server.")

    return response


def query_add_pstructure(obj: PriceStructure) -> tuple[bool, str]:
    response = (False, "Unknown Error")
    try:
        with Session() as s:
            try:
                s.add(obj)
                s.commit()
                response = (
                    True,
                    f'Price Structure "{obj.unique_code}" added successfully.',
                )
            except Exception as e:
                s.rollback()
                return (False, f"Execution failed.\n{e}")
    except:
        return (False, "Cannot establish connection with server.")

    return response


def query_update_pstructure(obj: PriceStructure) -> tuple[bool, str]:
    """Updates only basic rate"""

    response = (False, "Unknown Error")
    try:
        with Session() as s:
            try:
                update_obj: PriceStructure = (
                    s.query(PriceStructure)
                    .filter(
                        sa.and_(
                            PriceStructure.ps_code == obj.ps_code,
                            PriceStructure.mrp == obj.mrp,
                        )
                    )
                    .one()
                )
                update_obj.basic = obj.basic
                s.commit()
                response = (
                    True,
                    f'Basic rate for "{obj.unique_code}" updated successfully.',
                )
            except Exception as e:
                s.rollback()
                return (False, f"Execution failed.\n{e}")
    except:
        return (False, "Cannot establish connection with server.")

    return response


def query_delete_pstructure(obj: PriceStructure) -> tuple[bool, str]:
    """Delete only one Price Structure"""

    response = (False, "Unknown Error")
    try:
        with Session() as s:
            try:
                query = s.query(PriceStructure).filter(
                    sa.and_(
                        PriceStructure.ps_code == obj.ps_code,
                        PriceStructure.mrp == obj.mrp,
                    )
                )
                query.delete(synchronize_session=False)
                s.commit()
                response = (
                    True,
                    f"Successfully removed {obj.unique_code} from Price Structure.",
                )
            except Exception as e:
                s.rollback()
                return (False, f"Execution failed.\n{e}")
    except:
        return (False, "Cannot establish connection with server.")

    return response
