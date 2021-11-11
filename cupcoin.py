import pathlib
import csv

directory_path = pathlib.Path().resolve().absolute()
data_path = directory_path.joinpath('data/')


def load_data(file_name):
    block_chain = []
    file_path = data_path.joinpath(file_name)
    with open(file_path) as data_file:
        reader = csv.reader(data_file, )
        next(reader, None)
        for row in reader:
            code, block_number, from_address, to_address, value, block_timestamp = row
            transaction = {
                'transaction_code': code,
                'to_address': to_address,
                'from_address': from_address,
                'value': float(value),
                'operation': 'transfer' if to_address else 'contract'
            }

            block_chain.append(transaction)

    print(block_chain)


def add_transaction(chain, transaction):
    chain.append(transaction)


def close_block(chain, timestamp):
    pass


if __name__ == '__main__':
    load_data('cupicoin.csv')
