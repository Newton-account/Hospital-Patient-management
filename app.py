from flask import Flask, jsonify, request, render_template
from database import get_connection, init_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()


# ---------------- UI ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- MODEL ----------------
class Patient:
    def __init__(self, patient_id, nrc, name, age, severity, waiting_time, gender=None, phone=None, address=None):
        self.id = patient_id
        self.nrc = nrc
        self.name = name
        self.age = age
        self.severity = severity
        self.waiting_time = waiting_time
        self.gender = gender
        self.phone = phone
        self.address = address

    def to_dict(self):
        return self.__dict__


# ---------------- SORTING (Merge Sort) ----------------
def compare(a, b):
    if int(a.severity) != int(b.severity):
        return int(a.severity) < int(b.severity)
    return int(a.waiting_time) > int(b.waiting_time)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result + left[i:] + right[j:]


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


# ---------------- ADD PATIENT ----------------
@app.route("/patients", methods=["POST"])
def add_patient():
    data = request.json

    severity = str(data.get("severity", "")).strip()
    if severity not in ["1", "2", "3", "4", "5"]:
        return jsonify({"message": "Severity must be between 1 and 5"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients (nrc, name, age, severity, waiting_time, gender, phone, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["nrc"],
        data["name"],
        data.get("age"),
        severity,
        data["waiting_time"],
        data.get("gender"),
        data.get("phone"),
        data.get("address")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Patient saved successfully"})


# ---------------- GET PATIENTS ----------------
@app.route("/patients", methods=["GET"])
def get_patients():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nrc, name, age, severity, waiting_time, gender, phone, address
        FROM patients
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


# ---------------- DISCHARGE PATIENT ----------------
@app.route("/patients/<int:patient_id>", methods=["DELETE"])
def discharge_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Patient P{str(patient_id).zfill(3)} discharged successfully"})


# ---------------- SEARCH ----------------
@app.route("/search/<int:patient_id>")
def search(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nrc, name, age, severity, waiting_time, gender, phone, address
        FROM patients
        WHERE id=?
    """, (patient_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify(dict(row))

    return jsonify({"error": "Patient not found"}), 404


# ---------------- BED ALLOCATION ----------------
@app.route("/allocate/<int:beds>")
def allocate(beds):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nrc, name, age, severity, waiting_time, gender, phone, address
        FROM patients
    """)
    rows = cursor.fetchall()
    conn.close()

    patients = [
        Patient(
            row["id"],
            row["nrc"],
            row["name"],
            row["age"],
            row["severity"],
            row["waiting_time"],
            row["gender"],
            row["phone"],
            row["address"]
        )
        for row in rows
    ]

    sorted_patients = merge_sort(patients)
    allocated = sorted_patients[:beds]

    return jsonify([p.to_dict() for p in allocated])


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)