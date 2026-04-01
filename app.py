from flask import Flask, render_template, request, redirect, jsonify
from database import (
    create_table,
    add_patient,
    get_all_patients,
    delete_patient,
    update_patient,
    get_patient_by_id,
    search_patients,
    sort_by_severity
)
from hash_table import HashTable
from queue_module import PatientQueue
from stack_module import ActionStack
from linked_list import LinkedList
from binary_tree import BinarySearchTree
import json
import os

app = Flask(__name__)

# Initialize database
create_table()

# Initialize data structures
patient_hash_table = HashTable()
patient_queue = PatientQueue()
action_stack = ActionStack()
patient_linked_list = LinkedList()
patient_tree = BinarySearchTree()

# Fixed hospital bed inventory
ALL_BEDS = [
    "B01", "B02", "B03", "B04", "B05",
    "B06", "B07", "B08", "B09", "B10",
    "ICU01", "ICU02", "ICU03", "ICU04", "ICU05"
]


def severity_label(severity):
    severity = int(severity)
    labels = {
        1: "1 - Mild",
        2: "2 - Moderate",
        3: "3 - Serious",
        4: "4 - Critical",
        5: "5 - Emergency"
    }
    return labels.get(severity, str(severity))


def get_allocated_beds():
    patients = get_all_patients()
    allocated = []

    for patient in patients:
        if patient["bed_number"] and patient["bed_status"] == "Allocated":
            allocated.append(patient["bed_number"])

    return allocated


def get_available_beds():
    allocated = get_allocated_beds()
    return [bed for bed in ALL_BEDS if bed not in allocated]


def load_all_structures():
    global patient_hash_table, patient_queue, patient_linked_list, patient_tree

    patient_hash_table = HashTable()
    patient_queue = PatientQueue()
    patient_linked_list = LinkedList()
    patient_tree = BinarySearchTree()

    patients = get_all_patients()
    print(f"[INFO] Loading structures with {len(patients)} patient(s)")

    for patient in patients:
        patient_hash_table.insert(patient["id"], patient)
        patient_queue.enqueue(patient)
        patient_linked_list.append(patient)
        patient_tree.insert(patient)


def import_sample_patients():
    patients = get_all_patients()

    if len(patients) > 0:
        return 0, "Database already has patients. No sample data imported."

    if not os.path.exists("sample_patients.json"):
        return 0, "sample_patients.json NOT FOUND in project folder."

    try:
        with open("sample_patients.json", "r", encoding="utf-8") as file:
            sample_data = json.load(file)

        inserted = 0
        for patient in sample_data:
            add_patient(
                patient["name"],
                patient["age"],
                patient["gender"],
                patient["phone"],
                patient["address"],
                patient["condition"],
                patient["severity"],
                "Waiting",
                patient.get("bed_number", ""),
                patient.get("bed_status", "Not Allocated")
            )
            inserted += 1

        load_all_structures()
        return inserted, f"Successfully imported {inserted} sample patient(s)."

    except Exception as e:
        return 0, f"Error importing sample patients: {str(e)}"


load_all_structures()


@app.route('/')
def index():
    patients = get_all_patients()
    return render_template('index.html', patients=patients, severity_label=severity_label)


@app.route('/beds')
def beds():
    allocated = get_allocated_beds()
    available = get_available_beds()

    return render_template(
        'beds.html',
        total_beds=len(ALL_BEDS),
        allocated_count=len(allocated),
        available_count=len(available),
        allocated_beds=allocated,
        available_beds=available,
        all_beds=ALL_BEDS
    )


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    phone = request.form['phone']
    address = request.form['address']
    condition = request.form['condition']
    severity = request.form['severity']
    bed_number = request.form.get('bed_number', '')
    bed_status = request.form.get('bed_status', 'Not Allocated')

    add_patient(name, age, gender, phone, address, condition, severity, "Waiting", bed_number, bed_status)
    action_stack.push(f"Added patient: {name}")
    load_all_structures()

    return redirect('/')


@app.route('/delete/<int:patient_id>')
def delete(patient_id):
    delete_patient(patient_id)
    action_stack.push(f"Deleted patient ID: {patient_id}")
    load_all_structures()
    return redirect('/')


@app.route('/discharge/<int:patient_id>')
def discharge(patient_id):
    patient = get_patient_by_id(patient_id)

    if not patient:
        return "Patient not found", 404

    update_patient(
        patient_id,
        patient["name"],
        patient["age"],
        patient["gender"],
        patient["phone"],
        patient["address"],
        patient["condition"],
        patient["severity"],
        "Discharged",
        "",
        "Released"
    )

    action_stack.push(f"Discharged patient ID: {patient_id}")
    load_all_structures()
    return redirect('/')


@app.route('/allocate-bed/<int:patient_id>', methods=['GET', 'POST'])
def allocate_bed(patient_id):
    patient = get_patient_by_id(patient_id)

    if not patient:
        return "Patient not found", 404

    available_beds = get_available_beds()

    # Allow current patient to keep their own bed (important for reallocation)
    if patient["bed_number"] and patient["bed_number"] not in available_beds:
        available_beds.append(patient["bed_number"])

    if request.method == 'POST':
        bed_number = request.form['bed_number']

        # Safety check: prevent assigning an already occupied bed
        if bed_number not in get_available_beds() and bed_number != patient["bed_number"]:
            return "Error: Bed already allocated to another patient", 400

        new_status = patient["status"]
        if patient["status"] == "Discharged":
            new_status = "Admitted"

        update_patient(
            patient_id,
            patient["name"],
            patient["age"],
            patient["gender"],
            patient["phone"],
            patient["address"],
            patient["condition"],
            patient["severity"],
            new_status,
            bed_number,
            "Allocated"
        )

        action_stack.push(f"Allocated bed {bed_number} to patient ID: {patient_id}")
        load_all_structures()
        return redirect('/')

    return render_template(
        'allocate_bed.html',
        patient=patient,
        available_beds=sorted(available_beds)
    )


@app.route('/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit(patient_id):
    patient = get_patient_by_id(patient_id)

    if not patient:
        return "Patient not found", 404

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        condition = request.form['condition']
        severity = request.form['severity']
        status = request.form['status']
        bed_number = request.form.get('bed_number', '')
        bed_status = request.form.get('bed_status', 'Not Allocated')

        update_patient(patient_id, name, age, gender, phone, address, condition, severity, status, bed_number, bed_status)
        action_stack.push(f"Updated patient ID: {patient_id}")
        load_all_structures()

        return redirect('/')

    return render_template('edit.html', patient=patient)


@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '').strip()

    if keyword == "":
        patients = get_all_patients()
    else:
        patients = search_patients(keyword)

    return render_template('index.html', patients=patients, severity_label=severity_label)


@app.route('/sort', methods=['GET'])
def sort():
    patients = sort_by_severity()
    return render_template('index.html', patients=patients, severity_label=severity_label)


@app.route('/load-sample')
def load_sample():
    inserted, message = import_sample_patients()
    return jsonify({
        "inserted": inserted,
        "message": message,
        "total_patients_now": len(get_all_patients())
    })


@app.route('/debug/patients')
def debug_patients():
    return jsonify(get_all_patients())


# ------------------------------
# DSA ROUTES
# ------------------------------

@app.route('/hash/<int:patient_id>')
def get_patient_from_hash(patient_id):
    patient = patient_hash_table.get(patient_id)
    if patient:
        return jsonify(patient)
    return jsonify({"error": "Patient not found"}), 404


@app.route('/hash-table')
def display_hash_table():
    return jsonify(patient_hash_table.display())


@app.route('/queue')
def display_queue():
    return jsonify(patient_queue.display())


@app.route('/stack')
def display_stack():
    return jsonify(action_stack.display())


@app.route('/linked-list')
def display_linked_list():
    return jsonify(patient_linked_list.display())


@app.route('/tree')
def display_tree():
    return jsonify(patient_tree.inorder_traversal())


@app.route('/tree/search/<int:severity>')
def search_tree(severity):
    patient = patient_tree.search(severity)
    if patient:
        return jsonify(patient)
    return jsonify({"error": "No patient found with that severity"}), 404


if __name__ == '__main__':
    app.run(debug=True)