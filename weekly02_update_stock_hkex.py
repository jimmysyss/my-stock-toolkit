import math
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entity.stock import Stock


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
            print(v)
        print('xxxxxxxxxxxxx')


    #stock_list = session.query(Stock).order_by(Stock.reuter).all()
    #for i, v in enumerate(stock_list):
        #print(v)
        #pass


if __name__ == '__main__':
    retrieve_from_hkex()
