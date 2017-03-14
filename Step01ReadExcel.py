from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entity.base import Base
from entity.stock import Stock

from openpyxl import load_workbook


def init_db():
    engine = create_engine('sqlite:///./stock.db', convert_unicode=True)
    Base.metadata.create_all(engine)

    # Sample Stock
    # stock = Stock()
    # stock.reuter = '0001.HK'
    # stock.bloomberg = '1:HK'
    # stock.isin = 'ABC1234567'

    wb = load_workbook(filename="data/isino.xlsx")
    ws = wb['ISIN']

    Session = sessionmaker(bind=engine)
    session = Session()

    # From A20 onwards, A => Long Name / B => ISIN / C => Stock Code / D => Type
    row = 20
    while ws.cell(row=row, column=1).value is not None:
        # Check for Type
        type = ws.cell(row=row, column=4).value
        if (type != 'ORD SH') and (type != 'TRT'):
            row += 1
            continue

        stock = Stock()
        stock.fullname = ws.cell(row=row, column=1).value
        stock.isin = ws.cell(row=row, column=2).value
        stockCode = ws.cell(row=row, column=3).value
        stock.reuter = "{:04}.HK".format(stockCode)
        stock.bloomberg = "{:d}:HK".format(stockCode)

        session.add(stock)
        row += 1

    session.commit()

if __name__ == '__main__':
    init_db()
