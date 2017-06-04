import petl

def etl():
    # Extract
    input_data = petl.fromxls(filename='data/SRRPT20170317.xls', sheet='SBNReport')

    # Transform
    trimmed_head_data = petl.skip(input_data, 4)

    print(trimmed_head_data)


if __name__ == '__main__':
    etl()
