import pathlib
import csv
import time


def load_data(file_name):
    block_chain = []
    directory_path = pathlib.Path().resolve()
    file_path = directory_path.joinpath(f'data/{file_name}')
    counter_block = -1
    with open(file_path) as data_file:
        reader = csv.reader(data_file)
        next(reader, None)
        for row in reader:
            code, block_number, from_address, to_address, value, block_timestamp = row

            transaction = {
                'code': code,
                'from_address': from_address,
                'to_address': to_address,
                'value': float(value),
                'operation': 'transfer' if to_address else 'contract'
            }

            if block_number != counter_block:
                counter_block += 1
                create_block(block_chain, int(block_timestamp))

            add_transaction(block_chain, transaction)

    print(block_chain[0])
    return block_chain


def transaction_to_string(transaction):
    return (f"{transaction['code']}{transaction['from_address']}{transaction['to_address']}"
            f"{transaction['value']}{transaction['operation']}")


def get_hash(block):
    # Concatenar las transacciones
    transactions_info_string = ''
    block_info_string = ''
    numeric_key = 0

    while numeric_key not in block:
        transactions_info_string += transaction_to_string(block[numeric_key])
        numeric_key += 1

    block_info_string = transactions_info_string + str(block['block_number']) + str(block['before_hash'])
    block_hash = 0

    for c in block_info_string:
        block_hash += ord(c)

    return block_hash % block['timestamp']


def add_transaction(block_chain, transaction):
    transaction_key_in_block = 0
    while(transaction_key_in_block in block_chain[-1]):
        transaction_key_in_block += 1

    block_chain[-1][transaction_key_in_block] = transaction
    block_chain[-1]['transactions_count'] += 1


def create_block(block_chain, timestamp):
    new_block = {
        'block_number': 0,
        'transactions_count': 0,
        'timestamp': None,
        'open': True,
        'hash': 0,
        'before_hash': None,
    }

    if block_chain:
        # Cierre del bloque anterior
        last_block = block_chain[-1]
        last_block['open'] = False
        last_block['timestamp'] = timestamp
        last_block['hash'] = get_hash(last_block)
        # Apertura del nuevo bloque
        new_block['block_number'] = len(block_chain)
        new_block['before_hash'] = last_block['hash']
        block_chain.append(new_block)

    else:
        block_chain.append(new_block)


if __name__ == '__main__':
    load_data('cupicoin.csv')
