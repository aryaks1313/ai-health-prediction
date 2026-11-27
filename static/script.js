const API = "/api/patients";

let patients = [];
let editingId = null;
let liveMode = false;

const form = document.getElementById("patientForm");
const table = document.getElementById("patientTable");
const message = document.getElementById("message");
const saveButton = document.getElementById("saveButton");

const fields = [
    "full_name",
    "date_of_birth",
    "email",
    "glucose",
    "haemoglobin",
    "cholesterol"
];


function showMessage(text, type) {

    message.textContent = text;
    message.className = type;

}


async function request(url, options = {}) {

    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {

        let error = data.detail;

        if (Array.isArray(error)) {

            error = error.map(item => {

                const field = item.loc.at(-1);

                return `${field}: ${item.msg}`;

            }).join(" | ");
        }

        throw new Error(error || "Request failed.");
    }

    return data;
}


function formatDate(value) {

    const [year, month, day] = value.split("-");

    return `${day}/${month}/${year}`;
}


function renderPatients() {

    const search = document.getElementById("search")
        .value.toLowerCase();

    const filtered = patients.filter(patient =>

        patient.full_name.toLowerCase().includes(search)
        || patient.email.toLowerCase().includes(search)
    );

    table.replaceChildren();

    for (const p of filtered) {

        const tr = document.createElement("tr");

        const values = [
            p.full_name,
            formatDate(p.date_of_birth),
            p.email,
            p.glucose,
            p.haemoglobin,
            p.cholesterol,
            p.remarks
        ];

        for (const value of values) {

            const td = document.createElement("td");

            td.textContent = value;

            tr.appendChild(td);
        }

        const actions = document.createElement("td");

        const edit = document.createElement("button");

        edit.textContent = "Edit";
        edit.className = "edit";

        edit.addEventListener("click", () => {
            editPatient(p.id);
        });

        const remove = document.createElement("button");

        remove.textContent = "Delete";
        remove.className = "delete";

        remove.addEventListener("click", () => {
            deletePatient(p.id);
        });

        actions.append(edit, remove);

        tr.appendChild(actions);

        table.appendChild(tr);
    }

    document.getElementById("totalPatients")
        .textContent = patients.length;

    document.getElementById("totalAssessments")
        .textContent = patients.filter(

            p => p.remarks
                && !p.remarks.startsWith("DEMO MODE:")
        ).length;
}


async function loadPatients() {

    patients = await request(API);

    renderPatients();
}


async function checkHealth() {

    try {

        const health = await request("/api/health");

        liveMode = health.ai_mode === "live";

        document.getElementById("systemStatus")
            .textContent = liveMode
                ? "Running"
                : "Demo Mode";

    } catch {

        document.getElementById("systemStatus")
            .textContent = "Offline";
    }
}


form.addEventListener("submit", async event => {

    event.preventDefault();

    const patient = {};

    for (const field of fields) {

        patient[field] =
            document.getElementById(field).value;
    }

    const isEditing = editingId !== null;

    const url = isEditing
        ? `${API}/${editingId}`
        : API;

    const method = isEditing ? "PUT" : "POST";

    saveButton.disabled = true;
    saveButton.textContent = "Processing...";

    showMessage("Processing patient record...", "");

    try {

        await request(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(patient)
        });

        resetForm();

        showMessage(
            isEditing
                ? "Patient updated successfully."
                : "Patient created successfully.",
            "success"
        );

        await loadPatients();

    } catch (error) {

        showMessage(error.message, "error");

    } finally {

        saveButton.disabled = false;

        saveButton.textContent =
            editingId === null
                ? "Predict & Save Patient"
                : "Update Patient";
    }
});


async function editPatient(id) {

    try {

        const patient = await request(`${API}/${id}`);

        editingId = id;

        for (const field of fields) {

            document.getElementById(field).value =
                field === "date_of_birth"
                    ? formatDate(patient[field])
                    : patient[field];
        }

        document.getElementById("formTitle")
            .textContent = "Edit Patient";

        saveButton.textContent = "Update Patient";

        form.scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        showMessage(error.message, "error");
    }
}


async function deletePatient(id) {

    if (!confirm("Delete this patient record?")) {

        return;
    }

    try {

        await request(`${API}/${id}`, {
            method: "DELETE"
        });

        if (editingId === id) {

            resetForm();
        }

        showMessage(
            "Patient deleted successfully.",
            "success"
        );

        await loadPatients();

    } catch (error) {

        showMessage(error.message, "error");
    }
}


function resetForm() {

    form.reset();

    editingId = null;

    document.getElementById("formTitle")
        .textContent = "Register Patient";

    saveButton.textContent = "Predict & Save Patient";

    message.textContent = "";
    message.className = "";
}


document.getElementById("clearButton")
    .addEventListener("click", resetForm);

document.getElementById("search")
    .addEventListener("input", renderPatients);


async function initialize() {

    await checkHealth();

    try {

        await loadPatients();

    } catch (error) {

        showMessage(error.message, "error");
    }
}

initialize();