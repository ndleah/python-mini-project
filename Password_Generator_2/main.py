import argparse
from password_generator import generate_password

def main():
    parser = argparse.ArgumentParser(description='Generate a secure password')
    parser.add_argument('-l', '--length', type=int, default=12, help='Length of the password')
    parser.add_argument('-u', '--use_uppercase', action='store_true', default=True, help='Include uppercase letters')
    parser.add_argument('-lc', '--use_lowercase', action='store_true', default=True, help='Include lowercase letters')
    parser.add_argument('-n', '--use_numbers', action='store_true', default=True, help='Include numbers')
    parser.add_argument('-s', '--use_symbols', action='store_true', default=True, help='Include special symbols')

    args = parser.parse_args()

    password = generate_password(args.length, args.use_uppercase, args.use_lowercase, args.use_numbers, args.use_symbols)
    print(f'Generated Password: {password}')

if __name__ == '__main__':
    main()
