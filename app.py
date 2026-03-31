# from flask import Flask, jsonify, request, render_template
# import sqlite3
# # from flask_cors import CORS
# # CORS(app)

# app = Flask(__name__)
# @app.route("/")
# def home():
#     return render_template("index.html")

# # ---- Patient Model ----
# class Patient:
#     def __init__(self, patient_id, name, severity, waiting_time):
#         self.id = patient_id
#         self.name = name
#         self.severity = severity
#         self.waiting_time = waiting_time

#     def to_dict(self):
#         return self.__dict__


# patients = []


# # ---- Merge Sort ----
# def merge_sort(arr):
#     if len(arr) <= 1:
#         return arr

#     mid = len(arr)//2
#     left = merge_sort(arr[:mid])
#     right = merge_sort(arr[mid:])

#     return merge(left, right)


# def merge(left, right):
#     result = []
#     i = j = 0

#     while i < len(left) and j < len(right):
#         if compare(left[i], right[j]):
#             result.append(left[i])
#             i += 1
#         else:
#             result.append(right[j])
#             j += 1

#     return result + left[i:] + right[j:]


# def compare(a, b):
#     if a.severity != b.severity:
#         return a.severity < b.severity
#     return a.waiting_time > b.waiting_time


# # ---- Routes ----

# @app.route("/patients", methods=["POST"])
# def add_patient():
#     data = request.json

#     conn = sqlite3.connect("hospital.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO patients (id, name, severity, waiting_time)
#         VALUES (?, ?, ?, ?)
#     """, (data["id"], data["name"], data["severity"], data["waiting_time"]))

#     conn.commit()
#     conn.close()

#     return jsonify({"message": "Patient saved to database"})


# @app.route("/patients", methods=["GET"])
# def get_patients():
#     conn = sqlite3.connect("hospital.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT id, name, severity, waiting_time FROM patients")
#     rows = cursor.fetchall()
#     conn.close()

#     patients_list = [
#         Patient(r[0], r[1], r[2], r[3]) for r in rows
#     ]

#     sorted_list = merge_sort(patients_list)

#     return jsonify([p.to_dict() for p in sorted_list])


# @app.route("/search/<int:patient_id>")
# def search(patient_id):
#     conn = sqlite3.connect("hospital.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT id, name, severity, waiting_time FROM patients WHERE id=?", (patient_id,))
#     row = cursor.fetchone()

#     conn.close()

#     if row:
#         return jsonify(Patient(row[0], row[1], row[2], row[3]).to_dict())

#     return jsonify({"error": "Not found"}), 404


# @app.route("/allocate/<int:beds>")
# def allocate(beds):
#     conn = sqlite3.connect("hospital.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT id, name, severity, waiting_time FROM patients")
#     rows = cursor.fetchall()
#     conn.close()

#     patients_list = [Patient(*r) for r in rows]
#     sorted_list = merge_sort(patients_list)

#     allocated = sorted_list[:beds]

#     return jsonify([p.to_dict() for p in allocated])

# import sqlite3

# #create db and table fields
# def init_db():
#     conn = sqlite3.connect("hospital.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS patients (
#         id INTEGER PRIMARY KEY,
#         name TEXT,
#         severity INTEGER,
#         waiting_time INTEGER
#     )
#     """)

#     conn.commit()
#     conn.close()


# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)


from flask import Flask, jsonify, request, render_template
from database import get_connection
from flask_cors import CORS

app = Flask(__name__)

# ---------------- UI ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- MODEL ----------------
class Patient:
    def __init__(self, patient_id,nrc, name, severity, waiting_time):
        self.id = patient_id
        self.nrc = nrc
        self.name = name
        self.nrc = self.nrc
        self.severity = severity
        self.waiting_time = waiting_time

    def to_dict(self):
        return self.__dict__


# ---------------- SORTING (Merge Sort) ----------------
def compare(a, b):
    if a.severity != b.severity:
        return a.severity < b.severity
    return a.waiting_time > b.waiting_time


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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients (nrc, name, severity, waiting_time)
        VALUES (?, ?, ?, ?)
    """, (data["nrc"], data["name"], data["severity"], data["waiting_time"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Patient saved successfully"})


# ---------------- GET PATIENTS (SORTED) ----------------
@app.route("/patients", methods=["GET"])
def get_patients():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id,nrc, name, severity, waiting_time FROM patients")
    rows = cursor.fetchall()
    conn.close()

    patients = [Patient(*r) for r in rows]
    sorted_patients = merge_sort(patients)

    return jsonify([p.to_dict() for p in sorted_patients])


# ---------------- SEARCH ----------------
@app.route("/search/<int:patient_id>")
def search(patient_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, severity, waiting_time 
        FROM patients WHERE id=?
    """, (patient_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify(Patient(*row).to_dict())

    return jsonify({"error": "Patient not found"}), 404


# ---------------- BED ALLOCATION ----------------
@app.route("/allocate/<int:beds>")
def allocate(beds):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, severity, waiting_time FROM patients")
    rows = cursor.fetchall()
    conn.close()

    patients = merge_sort([Patient(*r) for r in rows])

    allocated = patients[:beds]

    return jsonify([p.to_dict() for p in allocated])


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
