import sys

# Offline Exchange Rates Fallback Table (Base: USD)
FALLBACK_RATES_USD = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.79,
    'INR': 83.2,
    'JPY': 155.4,
    'CAD': 1.36,
    'AUD': 1.51,
    'CHF': 0.91,
    'CNY': 7.23
}

CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'INR': '₹',
    'JPY': '¥',
    'CAD': 'CA$',
    'AUD': 'A$',
    'CHF': 'CHF',
    'CNY': '¥'
}

def get_symbol(currency_code: str) -> str:
    """Return currency symbol or currency code string."""
    code = currency_code.upper().strip()
    return CURRENCY_SYMBOLS.get(code, f" {code} ")

def convert_currency(amount: float = 1.0, base_cur: str = "USD", dest_cur: str = "EUR") -> float:
    """Convert amount between two currency codes using live API or offline rate table."""
    base = base_cur.upper().strip()
    dest = dest_cur.upper().strip()

    try:
        from forex_python.converter import CurrencyRates
        converter = CurrencyRates()
        return round(converter.convert(base_cur=base, dest_cur=dest, amount=amount), 3)
    except Exception:
        pass

    # Use offline fallback table
    if base in FALLBACK_RATES_USD and dest in FALLBACK_RATES_USD:
        usd_amount = amount / FALLBACK_RATES_USD[base]
        converted = usd_amount * FALLBACK_RATES_USD[dest]
        return round(converted, 3)
    elif base == dest:
        return round(amount, 3)
    else:
        print(f"Notice: Offline conversion for {base}->{dest} estimated at 1-to-1.")
        return round(amount, 3)

def parse_args(args_list: list) -> tuple:
    """Parse amount, base currency, and destination currency safely from CLI arguments."""
    if not args_list:
        return 1.0, "USD", "EUR"

    if len(args_list) >= 4 and args_list[2].lower() == 'to':
        try:
            amt = float(args_list[0])
            return amt, args_list[1].upper(), args_list[3].upper()
        except ValueError:
            pass

    if len(args_list) >= 3 and args_list[1].lower() == 'to':
        return 1.0, args_list[0].upper(), args_list[2].upper()

    return 1.0, "USD", "EUR"

def main():
    cli_args = sys.argv[1:]
    if not cli_args:
        print("Usage: currency-converter.py [<amount>] <BASE> to <DESTINATION>")
        print("Example: currency-converter.py 100 USD to EUR\n")

    amount, base, dest = parse_args(cli_args)
    base_sym = get_symbol(base)
    dest_sym = get_symbol(dest)

    res = convert_currency(amount, base, dest)
    print(f"💵 {amount}{base_sym} equals {res}{dest_sym}")

if __name__ == '__main__':
    main()

