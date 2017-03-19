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
        stock_list = session.query(Stock).order_by(Stock.reuter).limit(100).offset(batch*100).all()
        for i, v in enumerate(stock_list):
            target_url = HKEX_LINK.format(v.exchange)
            f = requests.get(target_url)
            soup = BeautifulSoup(f.text, 'lxml')
            tr_list = soup.find_all('tr')
            for j, tr in enumerate(tr_list):
                td_list = tr.find_all('td')
                if len(td_list)==0:
                    continue
                td = td_list[0]
                print(td.get_text())
                if (td.get_text().trim().startswith('Issued Shares:')):
                    print(td)
        print('xxxxxxxxxxxxx')




if __name__ == '__main__':
    retrieve_from_hkex()
