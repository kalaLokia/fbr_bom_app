"""
Models in the database

"""

import sqlalchemy as sa
from sqlalchemy.engine import URL

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import UniqueConstraint, PrimaryKeyConstraint  # , ForeignKey
from . import (
    SQL_T_ARTICLE,
    SQL_T_BOM,
    SQL_T_PRICE_STRUCTURE,
    SQL_T_CHARGES,
)  # , SQL_CONN

conn_string = (
    r"Driver={ODBC Driver 17 for SQL Server};"
    r"Server=localhost;"
    r"Database=production;"
    r"uid=sa;"
    r"pwd=kalalokia;"
    r"Integrated Security=false;"
)
conn_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_string})

engine = sa.create_engine(conn_url, connect_args={"timeout": 5})

Base = declarative_base()


class Bom(Base):
    """Model for Bom table"""

    __tablename__ = SQL_T_BOM

    index = sa.Column(sa.BIGINT(), primary_key=True, autoincrement=False)
    father = sa.Column(sa.VARCHAR(32))
    child = sa.Column(sa.VARCHAR(32))
    child_qty = sa.Column(sa.FLOAT(5))
    process = sa.Column(sa.VARCHAR(50))
    process_order = sa.Column(sa.INTEGER())
    child_item = sa.Column(sa.Text())
    child_uom = sa.Column(sa.VARCHAR(10))
    child_rate = sa.Column(sa.FLOAT(5))
    child_type = sa.Column(sa.VARCHAR(50))
    application = sa.Column(sa.VARCHAR(8))

    __table_args__ = (UniqueConstraint("father", "child", name="_unique_bom"),)


class Article(Base):
    """Model for Article table"""

    __tablename__ = SQL_T_ARTICLE

    sap_code = sa.Column(sa.VARCHAR(32), primary_key=True)
    product_type = sa.Column(sa.VARCHAR(50))
    mrp = sa.Column(sa.FLOAT(2))
    pairs_in_case = sa.Column("no_of_pairs", sa.INTEGER())
    size_matrix = sa.Column(sa.VARCHAR(6))
    brand = sa.Column(sa.VARCHAR(32))
    art_no = sa.Column(sa.VARCHAR(8))
    color = sa.Column(sa.VARCHAR(32))
    category = sa.Column(sa.VARCHAR(10))
    color_code = sa.Column(sa.CHAR(2))
    category_code = sa.Column(sa.CHAR(1))
    ps_code = sa.Column("price_structure", sa.CHAR(1))
    article = sa.Column(sa.VARCHAR(128))
    article_code = sa.Column(sa.VARCHAR(16))

    @property
    def size(self) -> int:
        common_size = {"g": 8, "l": 7, "x": 11, "c": 12, "k": 10, "b": 3, "r": 3}
        return common_size.get(self.category_code, 8)


class OSCharges(Base):
    """Model for OS Charges"""

    __tablename__ = SQL_T_CHARGES

    article = sa.Column(sa.VARCHAR(16), primary_key=True)  # same as article_code
    stitch_rate = sa.Column("stitching", sa.FLOAT(2))
    print_rate = sa.Column("printing", sa.FLOAT(2))


class PriceStructure(Base):
    """Model for OS Charges"""

    __tablename__ = SQL_T_PRICE_STRUCTURE

    ps_code = sa.Column("price_structure", sa.CHAR(1))  # same as article_code
    mrp = sa.Column(sa.FLOAT(2))
    basic = sa.Column(sa.FLOAT(2))

    __table_args__ = (
        PrimaryKeyConstraint(ps_code, mrp),
        {},
    )


Base.metadata.create_all(engine)
