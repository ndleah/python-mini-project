import qrcode
import os
import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def create_students_table(connection):
    try:
        cursor = connection.cursor()

        # Define the table creation query
        table_query = """
        CREATE TABLE IF NOT EXISTS students (
            UId INT PRIMARY KEY,
            Name VARCHAR(255),
            Roll INT,
            Class VARCHAR(50),
            Attendance varchar(10),
            Timestamp TIMESTAMP DEFAULT NULL
        )
        """

        # Execute the table creation query
        cursor.execute(table_query)
        print("Table 'students' created or already exists.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()


def insert_student_data(connection, data):
    try:
        cursor = connection.cursor()

        # Define the SQL query for inserting data
        insert_query = """
        INSERT INTO students (UId, Name, Roll, Class)
        VALUES (%s, %s, %s, %s)
        """

        # Insert each data entry into the table
        for entry in data:
            cursor.execute(insert_query, entry)

        # Commit the changes
        connection.commit()
        print("Data inserted into 'students' table.")

    except Error as e:
        connection.rollback()
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()


def generate_qr_code(data, output_folder="qrcodes"):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for entry in data:
        uid, name, roll, class_ = entry
        # Combine data into a string
        data_string = f"UId: {uid}\nName: {name}\nRoll: {roll}\nClass: {class_}"

        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Add data to QR code
        qr.add_data(data_string)
        qr.make(fit=True)

        # Create an image from the QR code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a file in the output folder
        filename = os.path.join(output_folder, f"{uid}.png")
        img.save(filename)
        print(f"QR code for UId {uid} saved as {filename}")


def get_data_recursively(exit_flag="exit"):
    data_list = []
    while True:
        user_input = input("Enter data in the format [UId,Name,Roll,Class] (enter 'exit' to finish): ")

        # Check if the user wants to exit
        if user_input.lower() == exit_flag.lower():
            break

        # Convert the input string to a list
        try:
            data_entry = eval(user_input)
            if len(data_entry) == 4:
                data_list.append(data_entry)
            else:
                print("Invalid input. Please provide data in the correct format.")
        except:
            print("Invalid input. Please provide data in the correct format.")

    return data_list


if __name__ == "__main__":
    # Get data input from the user recursively
    data_list = get_data_recursively()

    # Establish a connection to the MySQL database
    connection = create_connection()

    if connection:
        # Create 'students' table if not exists
        create_students_table(connection)

        # Insert data into the 'students' table
        if data_list:
            insert_student_data(connection, data_list)

            # Generate QR codes
            generate_qr_code(data_list)

        # Close the database connection
        connection.close()
