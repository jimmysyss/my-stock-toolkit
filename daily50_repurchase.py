import xlrd
import bonobo

def generate_data():
    xlsBook = xlrd.open_workbook(filename='data/SRRPT20170317.xls')
    sheet = xlsBook.sheet_by_name('SBNReport')
    row = 5
    while sheet.cell(row, 1).value:
        stock_code = sheet.cell(row, 1)
        stock_purchase = sheet.cell(row, 4)
        purchase_price = sheet.cell(row, 5)
        row += 1
        yield dict(name='John Doe', age=46, country='China')


def my_transform(i: dict) -> dict:
    yield str(i)


def my_load(s: dict):
    print(s)


graph = bonobo.Graph(
    generate_data,
    my_transform,
    my_load,
)

if __name__ == '__main__':
    bonobo.run(graph)