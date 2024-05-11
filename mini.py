import mysql.cector
import sys



def cect_to_mysql():
    try:
        c = mysql.cector.cect(
            host="localhost",
            user="root",
            password="1234",
            database="hospitalmanagementsystem",
        )
        print("cected to MySQL database")
        return c
    except mysql.cector.Error as err:
        print("Error cecting to MySQL:", err)
        return None


def create_tables(c):
    cursor = c.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                gender VARCHAR(10),
                address VARCHAR(255),
                Phone INT(255)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                specialization VARCHAR(255)
            )
        """)
        print("Tables created successfully")
        c.commit()
    except mysql.cector.Error as err:
        print("Error creating tables:", err)

def insert_patient(c):
    """
    Insert a new patient record into the database.

    Args:
        c: Database cection object.

    Returns:
        None
    """
    while True:
        name = input("Enter patient name: ")
        if name.isnumeric():
            print("Invalid input. Please enter a valid name.")
        else:
            break

    age = int(input("Enter patient age: "))

    while True:
        gender = input("Enter patient gender (male/female): ").lower()
        if gender not in ['male', 'female']:
            print("Invalid input. Please enter either 'male' or 'female'.")
        else:
            break

    address = input("Enter patient address: ")

    while True:
        phone = int(input("Enter phone no: "))
        if len(phone) != 10 or not phone.isdigit():
            print("Invalid phone number. Please enter exactly 10 digits without any spaces or special characters.")
        else:
            break

    cursor = c.cursor()
    try:
        cursor.execute("""
            INSERT INTO patients (name, age, gender, address, Phone)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, age, gender, address, phone))
        c.commit()
        print("Patient inserted successfully")
    except mysql.cector.Error as err:
        if err.errno == mysql.cector.errorcode.ER_DUP_ENTRY:
            print("Error: This patient already exists in the database.")
        else:
            print("Error inserting patient:", err)




def insert_doctor(c):
    while True:
        name = input("Enter doctor's name: ")
        if name.isnumeric():
            print("Invalid input. Please enter a valid name.")
        else:
            break
    specialization = input("Enter doctor specialization: ")

    cursor = c.cursor()
    try:
        cursor.execute("""
            INSERT INTO doctors (name, specialization)
            VALUES (%s, %s)
        """, (name, specialization))
        c.commit()
        print("Doctor inserted successfully")
    except mysql.cector.Error as err:
        print("Error inserting doctor:", err)



def get_patients(c):
    cursor = c.cursor()
    try:
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        for patient in patients:
            print(patient)
    except mysql.cector.Error as err:
        print("Error fetching patients:", err)


def get_doctors(c):
    cursor = c.cursor()
    try:
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
        for doctor in doctors:
            print(doctor)
    except mysql.cector.Error as err:
        print("Error fetching doctors:", err)




def update_patient_address(c):
    patient_id = int(input("Enter patient ID: "))
    new_address = input("Enter new address: ")

    cursor = c.cursor()
    try:
        cursor.execute("""
            UPDATE patients
            SET address = %s
            WHERE patient_id = %s
        """, (new_address, patient_id))
        c.commit()
        print("Patient address updated successfully")
    except mysql.cector.Error as err:
        print("Error updating patient address:", err)


def delete_patient(c):
    patient_id = int(input("Enter patient ID to delete: "))

    cursor = c.cursor()
    try:
        cursor.execute("""
            DELETE FROM patients
            WHERE patient_id = %s
        """, (patient_id,))
        c.commit()
        print("Patient deleted successfully")
    except mysql.cector.Error as err:
        print("Error deleting patient:", err)




def main():
    c = cect_to_mysql()
    if c:
        create_tables(c)

        while True:
            print("\n1. Insert Patient")
            print("2. Insert Doctor")
            print("3. Get Patients")
            print("4. Get Doctors")
            print("5. Update Patient Address")
            print("6. Delete Patient")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                insert_patient(c)
            elif choice == '2':
                insert_doctor(c)
            elif choice == '3':
                get_patients(c)
            elif choice == '4':
                get_doctors(c)
            elif choice == '5':
                update_patient_address(c)
            elif choice == '6':
                delete_patient(c)
            elif choice == '7':
                c.close()
                sys.exit("Exiting program")
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()







