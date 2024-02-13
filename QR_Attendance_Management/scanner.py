import cv2
from pyzbar.pyzbar import decode
import mysql.connector
from datetime import datetime

# Set to keep track of logged-in students
logged_in_students = set()

# Set to keep track of already scanned QR codes
scanned_qrs = set()

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "project"
}

cn = mysql.connector.connect(**db_config)
cur = cn.cursor()
cur.execute('update students set attendance="Absent",timestamp=NULL;')
cn.commit()
cn.close()


def log_attendance(student_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the student exists in the student table
        check_student_sql = "SELECT uid FROM students WHERE uid = %s"
        cursor.execute(check_student_sql, (student_id,))
        student_exists = cursor.fetchone()

        scan_timestamp = datetime.now()

        if student_exists:
            # Check if the QR code has already been scanned
            if student_id not in scanned_qrs:
                # Update the attendance and timestamp in the students table
                update_student_sql = "UPDATE students SET attendance = 'Present', timestamp = %s WHERE uid = %s"
                update_student_values = (scan_timestamp, student_id)
                cursor.execute(update_student_sql, update_student_values)

                logged_in_students.add(student_id)
                scanned_qrs.add(student_id)
                print(f"Attendance updated successfully for {student_id}!")

        else:
            print(f"Student with UID {student_id} not found in the student table. Attendance not updated.")
            scan_timestamp = '-'

        connection.commit()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        scan_timestamp = '-'

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

        return scan_timestamp


# Start the camera
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()

    # Decode QR codes in the frame
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        qr_data_lines = obj.data.decode('utf-8').split('\n')

        # Extract numeric part (student ID) from the first line of the QR code data
        numeric_part = ''.join(filter(str.isdigit, qr_data_lines[0]))

        if numeric_part:
            # Assuming the numeric part is the student ID
            student_id = int(numeric_part)

            # Log attendance into MySQL and get the scan timestamp
            scan_timestamp = log_attendance(student_id)

            # Display the scan timestamp on the frame
            cv2.putText(frame, f"Scan Time: {datetime.now()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                        2)

    # Display the frame
    cv2.imshow("QR Code Scanner", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
