import argparse
from password_generator import generate_password

def main():
    parser = argparse.ArgumentParser(description='Generate a secure password')
    parser.add_argument('-l', '--length', type=int, default=12, help='Length of the password (default: 12)')
    parser.add_argument('--no-uppercase', dest='use_uppercase', action='store_false', help='Exclude uppercase letters')
    parser.add_argument('--no-lowercase', dest='use_lowercase', action='store_false', help='Exclude lowercase letters')
    parser.add_argument('--no-numbers', dest='use_numbers', action='store_false', help='Exclude numbers')
    parser.add_argument('--no-symbols', dest='use_symbols', action='store_false', help='Exclude special symbols')

    args = parser.parse_args()

    try:
        password = generate_password(
            length=args.length,
            use_uppercase=args.use_uppercase,
            use_lowercase=args.use_lowercase,
            use_numbers=args.use_numbers,
            use_symbols=args.use_symbols
        )
        print(f'Generated Password: {password}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()

