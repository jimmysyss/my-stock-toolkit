import xlrd
import bonobo
import dataset

#db = dataset.connect('sqlite:///./stock.db')
#table = db['repurchases']

def generate_data():
    xlsBook = xlrd.open_workbook(filename='data/SRRPT20170317.xls')
    sheet = xlsBook.sheet_by_name('SBNReport')
    row = 5
    while sheet.cell(row, 1).value:
        stock_code = sheet.cell(row, 1).value
        stock_purchase = sheet.cell(row, 4).value
        purchase_price = sheet.cell(row, 5).value
        row += 1
        yield dict(stock_code=stock_code, stock_purchase=stock_purchase, purchase_price=purchase_price)


def my_transform(i: dict) -> dict:
    new_dict = dict(
        stock_code=i['stock_code'],
        stock_purchase=int(i['stock_purchase'].replace(",", "")),
        purchase_price=float(i['purchase_price'].split()[1]),
    )
    yield new_dict


def my_load(s: dict):
    # print(s)
    db = dataset.connect('sqlite:///./stock.db')
    print('HELLO')
    table = db['repurchases']
    table.insert(s)


graph = bonobo.Graph(
    generate_data,
    my_transform,
    my_load,
)

if __name__ == '__main__':
    bonobo.run(graph)