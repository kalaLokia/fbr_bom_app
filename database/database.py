"""
Models in the database

"""

import sqlalchemy as sa
from sqlalchemy.engine import URL

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import UniqueConstraint, PrimaryKeyConstraint  # , ForeignKey
from . import (
    SQL_DB_NAME,
    SQL_T_ARTICLE,
    SQL_T_BOM,
    SQL_T_PRICE_STRUCTURE,
    SQL_T_CHARGES,
    SQL_T_FIXED_RATES,
)  # , SQL_CONN

conn_string = (
    r"Driver={ODBC Driver 17 for SQL Server};"
    r"Server=localhost;"
    rf"Database={SQL_DB_NAME};"
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

    bom_id = sa.Column(sa.BIGINT(), primary_key=True, autoincrement=False)
    father = sa.Column(sa.VARCHAR(32))
    child = sa.Column(sa.VARCHAR(32))
    child_qty = sa.Column(sa.FLOAT(5))
    process = sa.Column(sa.VARCHAR(50))
    process_order = sa.Column(sa.INTEGER())
    child_item = sa.Column(sa.Text())
    child_uom = sa.Column(sa.VARCHAR(10))
    child_rate = sa.Column(sa.FLOAT(3))
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
        common_size = {"g": 8, "l": 7, "x": 12, "c": 12, "k": 10, "b": 3, "r": 3}
        return common_size.get(self.category_code, 8)

    @property
    def get_filename(self):
        return self.article + "_mnf.xlsx"


class OSCharges(Base):
    """Model for OS Charges"""

    __tablename__ = SQL_T_CHARGES

    article = sa.Column(sa.VARCHAR(16), primary_key=True)  # same as article_code
    stitch_rate = sa.Column(
        "stitching", sa.FLOAT(2)
    )  # FIXME: Check the support, real coming as var
    print_rate = sa.Column("printing", sa.FLOAT(2))

    @property
    def stitching(self):
        return round(self.stitch_rate, 2)

    @property
    def printing(self):
        return round(self.print_rate, 2)


class PriceStructure(Base):
    """Model for OS Charges"""

    __tablename__ = SQL_T_PRICE_STRUCTURE

    ps_code = sa.Column("price_structure", sa.CHAR(1))  # same as article_code
    mrp = sa.Column(sa.FLOAT(2))
    basic = sa.Column(sa.FLOAT(2))

    @property
    def get_price_struct(self):
        return (
            {"p": "pride", "d": "debongo", "s": "stile"}
            .get(self.ps_code.lower(), "pride")
            .title()
        )

    def to_ps_code(self, text: str):
        self.ps_code = {"pride": "P", "debongo": "D", "stile": "S"}.get(
            text.strip().lower(), "P"
        )

    @property
    def unique_code(self):
        return f"{self.get_price_struct}-{self.mrp}"

    __table_args__ = (
        PrimaryKeyConstraint(ps_code, mrp),
        {},
    )


class FixedRates(Base):
    """Model for Fixed rates on cost"""

    __tablename__ = SQL_T_FIXED_RATES

    rates_id = sa.Column(sa.BIGINT(), primary_key=True, autoincrement=True)
    name = sa.Column(sa.VARCHAR(50), unique=True)
    value = sa.Column(sa.FLOAT(5))
    value_fmt = sa.Column(sa.VARCHAR(10))
    rate_type = sa.Column(sa.CHAR(2))  # OH: Overheads, OC: Other Charges


Base.metadata.create_all(engine)
