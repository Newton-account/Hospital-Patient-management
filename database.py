import sqlite3

DB_NAME = "hospital.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        condition TEXT NOT NULL,
        severity INTEGER NOT NULL,
        status TEXT NOT NULL,
        bed_number TEXT,
        bed_status TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_patient(name, age, gender, phone, address, condition, severity, status="Waiting", bed_number="", bed_status="Not Allocated"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patients (name, age, gender, phone, address, condition, severity, status, bed_number, bed_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, age, gender, phone, address, condition, severity, status, bed_number, bed_status))

    conn.commit()
    conn.close()


def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()
    return [dict(patient) for patient in patients]


def get_patient_by_id(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()

    conn.close()
    return dict(patient) if patient else None


def update_patient(patient_id, name, age, gender, phone, address, condition, severity, status, bed_number, bed_status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE patients
    SET name = ?, age = ?, gender = ?, phone = ?, address = ?, condition = ?, severity = ?, status = ?, bed_number = ?, bed_status = ?
    WHERE id = ?
    """, (name, age, gender, phone, address, condition, severity, status, bed_number, bed_status, patient_id))

    conn.commit()
    conn.close()


def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))

    conn.commit()
    conn.close()


def search_patients(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM patients
    WHERE name LIKE ? OR condition LIKE ? OR phone LIKE ? OR gender LIKE ? OR bed_number LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    patients = cursor.fetchall()
    conn.close()

    return [dict(patient) for patient in patients]


def sort_by_severity():
    """
    DSA Requirement: Sorting Algorithm
    Uses Insertion Sort to sort patients by severity (highest first)
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    patients = [dict(patient) for patient in patients]

    # Insertion Sort (Descending by severity)
    for i in range(1, len(patients)):
        key = patients[i]
        j = i - 1

        while j >= 0 and int(patients[j]["severity"]) < int(key["severity"]):
            patients[j + 1] = patients[j]
            j -= 1

        patients[j + 1] = key

    return patients
# final update