"""
SQL queries execution

"""

import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from .database import Bom, Article, OSCharges, PriceStructure, engine

# engine = sa.create_engine(SQL_CONN, echo=False, connect_args={"timeout": 5})

Session = sessionmaker(bind=engine)

# SELECT * FROM tbl_articles
# INNER JOIN tbl_price_structure ps ON ps.price_structure = tbl_articles.price_structure  AND ps.mrp = tbl_articles.mrp


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


def query_list_articles_all():
    """List all articles"""
    result = None
    with Session() as s:
        result = (
            s.query(
                Article.article,
                Article.sap_code,
                Article.mrp,
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


def query_articles_all():
    """List all articles"""
    result = None
    with Session() as s:
        result = (
            s.query(Article, PriceStructure, OSCharges)
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
            .all()
        )

    return result
