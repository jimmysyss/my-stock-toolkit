import enum

from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange = Column(String)
    reuter = Column(String, unique=True)
    bloomberg = Column(String, unique=True)
    isin = Column(String)
    fullname = Column(String)
    market_cap_ccy = Column(String)
    market_cap = Column(Integer)
    issue_share = Column(Integer)
    website = Column(String)


class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    stock = relationship('Stock', backref=backref('quotes', order_by=id))
    quote_date = Column(Date)
    quote_type = Column(Enum('daily', 'weekly', 'montly'))
    open = Column(Numeric)
    close = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    volumn_share = Column(Numeric)
    volumn_amount = Column(Numeric)
    UniqueConstraint('quote_date', 'stock', name='quotes_uk1')


class DailyInfo(Base):
    __tablename__ = 'daily_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    stock = relationship('Stock', backref=backref('daily_infos', order_by=id))
    info_date = Column(Date)
    UniqueConstraint('info_date', 'stock', name='daily_info_uk1')


def init_db():
    engine = create_engine('sqlite:///./stock1.db', convert_unicode=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
