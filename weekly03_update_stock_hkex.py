import math
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entity.stock import Stock

HKEX_LINK = 'https://www.hkex.com.hk/eng/invest/company/profile_page_e.asp?WidCoID={:s}&WidCoAbbName=&Month=&langcode=e'


def retrieve_from_hkex():
    engine = create_engine('sqlite:///./stock.db', convert_unicode=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # iterate for Stock
    batch_size = 100
    stock_count = session.query(Stock).count()

    print(stock_count)

    for batch in range(0, math.ceil(stock_count / batch_size)):
        stock_list = session.query(Stock).order_by(Stock.reuter).limit(100).offset(batch * 100).all()
        for i, stock in enumerate(stock_list):
            target_url = HKEX_LINK.format(stock.exchange)
            print(target_url)
            f = requests.get(target_url)
            soup = BeautifulSoup(f.text, 'lxml')
            tr_list = soup.find_all('tr')
            for j, tr in enumerate(tr_list):
                td_list = tr.find_all('td')
                if len(td_list) == 0:
                    continue
                td = td_list[0]

                if (td.get_text().strip().startswith('Issued Shares:')):
                    # print(td_list[1].get_text().split()[0])
                    stock.issue_share = int(td_list[1].get_text().split()[0].replace(',', ''))
                if (td.get_text().strip().startswith('Market Capitalisation:')):
                    # print(td_list[1].get_text().split()[0] + td_list[1].get_text().split()[1])
                    stock.market_cap_ccy = td_list[1].get_text().split()[0]
                    stock.market_cap = td_list[1].get_text().split()[1]
        session.commit()
        print(batch)


if __name__ == '__main__':
    retrieve_from_hkex()
