from converter_values import options, CATEGORIES

def main():
    print(options["help"])  # prints help menu
    res = input("Response: ").strip()

    while res.lower() != "q":  # program loop
        try:
            parts = res.split()

            if len(parts) == 1:
                display_help(parts[0])  # display help menu
            elif len(parts) == 4:
                perform_conversion(parts)  # perform unit conversion
            else:
                print("Invalid command. Type 'help' for options.")

        except Exception as e:
            print("Error:", e)

        res = input("\nResponse: ").strip()

def display_help(command):
    """Display help menu."""
    if command in options:
        print(options[command])
    else:
        print(f"Unknown command '{command}'. Type 'help' or 'symbols' for available options.")

def perform_conversion(res):
    """Perform unit conversion safely without eval."""
    cat_code = res[0].upper()
    from_unit = res[1]

    try:
        val = float(res[2])
    except ValueError:
        print(f"Invalid numerical value '{res[2]}'.")
        return

    if cat_code not in CATEGORIES:
        print(f"Invalid category '{res[0]}'. Available categories: {', '.join(CATEGORIES.keys())}.")
        return

    unit_dict = CATEGORIES[cat_code]

    if from_unit not in unit_dict:
        print(f"Invalid source unit '{from_unit}' for category {cat_code}.")
        return

    target_units = [u.strip() for u in res[3].split(',') if u.strip()]

    for target_unit in target_units:
        if target_unit not in unit_dict:
            print(f"Invalid target unit '{target_unit}' for category {cat_code}.")
            continue

        value = round(val * unit_dict[target_unit] / unit_dict[from_unit], 6)
        print("{} \t : {}".format(target_unit, value))

if __name__ == "__main__":
    main()



