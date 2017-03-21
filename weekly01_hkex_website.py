from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entity.base import Base
from entity.stock import Stock

from openpyxl import load_workbook

HKEX_SITE = 'http://www.hkexnews.hk/hyperlink/hyperlist.HTM'

def init_db():
    engine = create_engine('sqlite:///./stock.db', convert_unicode=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()



    session.commit()

if __name__ == '__main__':
    init_db()
