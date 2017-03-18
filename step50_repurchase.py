import xlrd

xlsBook = xlrd.open_workbook(filename='data/SRRPT20170317.xls')

sheet = xlsBook.sheet_by_name('SBNReport')

row = 5

while sheet.cell(row, 1).value:
    stock_code = sheet.cell(row, 1)
    stock_purchase = sheet.cell(row, 4)
    purchase_price = sheet.cell(row, 5)

    row += 1
