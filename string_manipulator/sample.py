from string_manipulator import StringManipulator

def main():
    my_string = "Hello, World!"
    manipulator = StringManipulator(my_string)

    print("Concatenated string:", manipulator.concatenate(" Goodbye"))
    print("Length of the string:", manipulator.length())
    print("Sliced string:", manipulator.slice(7, None))
    print("Repeated string:", manipulator.repeat(2))
    print("Uppercase:", manipulator.uppercase())
    print("Lowercase:", manipulator.lowercase())
    print("Stripped string:", StringManipulator("   Hello   ").strip())
    print("Split string:", manipulator.split(","))

    fmt_manipulator = StringManipulator("Hello, {}! You are {} years old.")
    print("Formatted string:", fmt_manipulator.format("Alice", 30))

    kw_manipulator = StringManipulator("Hello, {name}! You are {age} years old.")
    print("Interpolated string:", kw_manipulator.interpolate(name="Bob", age=25))

if __name__ == '__main__':
    main()

