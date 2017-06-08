import petl


def etl():
    # Extract
    input_data = petl.fromxls(filename='data/SRRPT20170317.xls', sheet='SBNReport')

    # Transform
    step1_data = petl.skip(input_data, 4)
    step2_data = petl.setheader(step1_data, \
                                   ['Company Name', 'Stock Code', 'Sec Type', 'Trade Date', 'Purchase Shares', \
                                    'Purchase Price', 'Lowest Price', 'X', 'Y', 'YTD Purchase', \
                                    'YTD Perc Outstanding'])
    step3_data = petl.select(step2_data, lambda rec: rec['Stock Code'] != '')
    step4_data = petl.convert(step3_data, {
        'Purchase Shares': lambda v: int(v.replace(",", "")),
        'Purchase Price': lambda v: float(v.split()[1]),
        'YTD Purchase': lambda v: int(v.replace(",", "")),
        'YTD Perc Outstanding': lambda v: float(v.split()[1])
    })

    # Write to DB
    print(petl.lookall(step4_data))


if __name__ == '__main__':
    etl()
