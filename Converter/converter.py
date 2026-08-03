from converter_values import options, CATEGORIES

def main():
    print(options["help"])  # prints help menu
    res = input("Response: ")

    while res.lower() != "q":  # program loop
        try:
            tokens = res.strip().split(" ")

            if len(tokens) == 1:
                display_help(tokens[0])  # display help menu
            elif len(tokens) == 4:
                perform_conversion(tokens)  # perform unit conversion
            else:
                print("Invalid command. Format: <Category> <Unit> <Value> <TargetUnits>")

        except Exception as e:
            print("Error:", e)

        res = input("\nResponse: ")

def display_help(command):
    """Display help menu."""
    if command in options:
        print(options[command])
    else:
        print(f"Unknown command '{command}'. Type 'help' or 'symbols'.")

def perform_conversion(res):
    """Perform unit conversion cleanly without unsafe eval."""
    category_code = res[0].upper()
    src_unit = res[1]
    
    if category_code not in CATEGORIES:
        print(f"Invalid category '{res[0]}'. Valid categories: {', '.join(CATEGORIES.keys())}")
        return

    unit_dict = CATEGORIES[category_code]
    
    if src_unit not in unit_dict:
        print(f"Invalid source unit '{src_unit}' for category '{category_code}'.")
        return

    try:
        raw_val = float(res[2])
    except ValueError:
        print(f"Invalid numeric value '{res[2]}'.")
        return

    target_units = [u.strip() for u in res[3].split(',')]
    for target in target_units:
        if target not in unit_dict:
            print(f"Invalid target unit '{target}' for category '{category_code}'.")
            continue
        
        # Calculation: val * unit_dict[target] / unit_dict[src_unit]
        calc_value = round((raw_val * unit_dict[target]) / unit_dict[src_unit], 6)
        print("{} \t : {}".format(target, calc_value))

if __name__ == "__main__":
    main()



