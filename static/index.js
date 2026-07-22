// ==============================
// API
// ==============================

const API = "http://127.0.0.1:8000";


// ==============================
// Edit IDs
// ==============================

let studentEditId = null;
let lessonEditId = null;


// ==============================
// Load Students
// ==============================

async function loadStudents() {

    const response = await fetch(`${API}/students`);

    const students = await response.json();

    const table = document.getElementById("studentsTable");

    const select = document.getElementById("studentsSelect");

    table.innerHTML = "";

    select.innerHTML = "";

    students.forEach(student => {

        table.innerHTML += `
        <tr>

            <td>${student.name}</td>

            <td>${student.phone}</td>

            <td>${student.age}</td>

            <td>
                <button onclick="editStudent(${student.id})">
                    تعديل
                </button>
            </td>

            <td>
                <button onclick="deleteStudent(${student.id})">
                    حذف
                </button>
            </td>

        </tr>
        `;

        select.innerHTML += `
            <option value="${student.id}">
                ${student.name}
            </option>
        `;

    });

}


// ==============================
// Load Lessons
// ==============================

async function loadLessons() {

    const response = await fetch(`${API}/lessons`);

    const lessons = await response.json();

    const table = document.getElementById("lessonsTable");

    const select = document.getElementById("lessonsSelect");

    table.innerHTML = "";

    select.innerHTML = "";

    lessons.forEach(lesson => {

        table.innerHTML += `
        <tr>

            <td>${lesson.title}</td>

            <td>${lesson.teacher}</td>

            <td>
                <button onclick="editLesson(${lesson.id})">
                    تعديل
                </button>
            </td>

            <td>
                <button onclick="deleteLesson(${lesson.id})">
                    حذف
                </button>
            </td>

        </tr>
        `;

        select.innerHTML += `
            <option value="${lesson.id}">
                ${lesson.title}
            </option>
        `;

    });

}


// ==============================
// Load Enrollments
// ==============================

async function loadEnrollments() {

    const response = await fetch(`${API}/enrollments`);

    const data = await response.json();

    const table = document.getElementById("enrollmentsTable");

    table.innerHTML = "";

    data.forEach(item => {

        table.innerHTML += `
        <tr>

            <td>${item.student}</td>

            <td>${item.lesson}</td>

            <td>${item.teacher}</td>

            <td>
                <button onclick="deleteEnrollment(${item.id})">
                    حذف
                </button>
            </td>

        </tr>
        `;

    });

}


// ==============================
// Save Student
// ==============================

async function saveStudent() {

    const name = document.getElementById("studentName").value;

    const phone = document.getElementById("studentPhone").value;

    const age = document.getElementById("studentAge").value;

    const data = {

        name,

        phone,

        age: Number(age)

    };

    if (studentEditId == null) {

        await fetch(`${API}/students`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });

    }

    else {

        await fetch(`${API}/students/${studentEditId}`, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });

        studentEditId = null;

    }

    document.getElementById("studentName").value = "";

    document.getElementById("studentPhone").value = "";

    document.getElementById("studentAge").value = "";

    loadStudents();

}


// ==============================
// Edit Student
// ==============================

async function editStudent(id) {

    const response = await fetch(`${API}/students`);

    const students = await response.json();

    const student = students.find(s => s.id == id);

    studentEditId = id;

    document.getElementById("studentName").value = student.name;

    document.getElementById("studentPhone").value = student.phone;

    document.getElementById("studentAge").value = student.age;

}


// ==============================
// Delete Student
// ==============================

async function deleteStudent(id) {

    await fetch(`${API}/students/${id}`, {

        method: "DELETE"

    });

    loadStudents();

    loadEnrollments();

}
// ==============================
// Save Lesson
// ==============================

async function saveLesson() {

    const title = document.getElementById("lessonTitle").value;
    const teacher = document.getElementById("lessonTeacher").value;

    const data = {
        title,
        teacher
    };

    if (lessonEditId == null) {

        await fetch(`${API}/lessons`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });

    }

    else {

        await fetch(`${API}/lessons/${lessonEditId}`, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });

        lessonEditId = null;

    }

    document.getElementById("lessonTitle").value = "";
    document.getElementById("lessonTeacher").value = "";

    loadLessons();

}


// ==============================
// Edit Lesson
// ==============================

async function editLesson(id) {

    const response = await fetch(`${API}/lessons`);

    const lessons = await response.json();

    const lesson = lessons.find(l => l.id == id);

    lessonEditId = id;

    document.getElementById("lessonTitle").value = lesson.title;
    document.getElementById("lessonTeacher").value = lesson.teacher;

}


// ==============================
// Delete Lesson
// ==============================

async function deleteLesson(id) {

    await fetch(`${API}/lessons/${id}`, {

        method: "DELETE"

    });

    loadLessons();

    loadEnrollments();

}


// ==============================
// Save Enrollment
// ==============================

async function saveEnrollment() {

    const student_id =
        Number(document.getElementById("studentsSelect").value);

    const lesson_id =
        Number(document.getElementById("lessonsSelect").value);

    if (!student_id || !lesson_id) {

        alert("اختر الطالب والدرس");

        return;

    }

    await fetch(`${API}/enrollments`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            student_id,
            lesson_id

        })

    });

    loadEnrollments();

}


// ==============================
// Delete Enrollment
// ==============================

async function deleteEnrollment(id) {

    await fetch(`${API}/enrollments/${id}`, {

        method: "DELETE"

    });

    loadEnrollments();

}


// ==============================
// Start Application
// ==============================

window.onload = () => {

    loadStudents();

    loadLessons();

    loadEnrollments();

};