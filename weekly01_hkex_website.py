import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entity.base import Base
from entity.stock import Stock

HKEX_SITE = 'http://www.hkexnews.hk/hyperlink/hyperlist.HTM'


def init_db():
    engine = create_engine('sqlite:///./stock.db', convert_unicode=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    print(HKEX_SITE)
    f = requests.get(HKEX_SITE)
    soup = BeautifulSoup(f.text, 'lxml')
    odd_tr_list = soup.find_all('tr', {"class": "ms-rteTableOddRow-BlueTable_ENG"})
    even_tr_list = soup.find_all('tr', {"class": "ms-rteTableEvenRow-BlueTable_ENG"})

    new_stock = 0
    update_stock = 0
    for j, tr in enumerate(odd_tr_list + even_tr_list):
        td_list = tr.find_all('td')

        # try to look up the message
        stock_code = int(td_list[0].get_text())
        reuter_code = "{:04}.HK".format(int(td_list[0].get_text()))
        existing_stock = session.query(Stock).filter_by(reuter=reuter_code).first()
        if existing_stock is None :
            # NEW
            stock = Stock(exchange=stock_code, reuter=reuter_code, website=td_list[2].get_text().strip())
            session.add(stock)
            new_stock += 1
        else:
            existing_stock.website = td_list[2].get_text().strip()
            update_stock += 1

    print('New {0} / Update {1}'.format(new_stock, update_stock))

    session.commit()

if __name__ == '__main__':
    init_db()
