from forex_python.converter import CurrencyRates, CurrencyCodes
from requests.exceptions import ConnectionError
from sys import argv

converter = CurrencyRates()
codes = CurrencyCodes()

def parse_arguments():
    amount = 1
    try:
        amount = float(argv[1])
        del argv[1]

    except ValueError:
        #no amount entered
        #default amount
        pass

    #argv:
    #[0] - program name
    #[1] - SRC
    #[2] - 'to'
    #[3] - DST
    if len(argv) != 4 or argv[2] != 'to':
        raise Exception

    return amount, argv[1].upper(), argv[3].upper()


#main
#parse arguments
usage = '[<amount>] <BASE> to <DESTINATION>'
try:
    amount, base, dest = parse_arguments()
except:
    print('usage:')
    print(usage)
    exit(1)

#convert
try:
    base_symbol = codes.get_symbol(base)
    dest_symbol = codes.get_symbol(dest)

    #validate currencies
    if base_symbol is None:
        raise Exception(f'Currency {base} is invalid')
    if dest_symbol is None:
        raise Exception(f'Currency {dest} is invalid')

    result = converter.convert(base_cur=base, dest_cur=dest, amount=amount)
    result = round(result, 3)

    print(f'{amount}{base_symbol} equals to {result}{dest_symbol}')

except ConnectionError as e:
    print('Connection error')
    exit(1)

except Exception as e:
    print(e.args[0])
    exit(1)
