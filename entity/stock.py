from sqlalchemy import Column, Integer, String

from entity.base import Base


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange = Column(String)
    reuter = Column(String)
    bloomberg = Column(String)
    isin = Column(String)
    fullname = Column(String)
    market_cap_ccy = Column(String)
    market_cap = Column(Integer)
    issue_share = Column(Integer)
    website = Column(String)
