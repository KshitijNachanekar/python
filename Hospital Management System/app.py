from flask import Flask, request, jsonify, render_template_string
import mysql.connector

app = Flask(__name__)

# =========================================
# DATABASE CONNECTION
# =========================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="hospital_db"
)

cursor = db.cursor(dictionary=True)

# =========================================
# CREATE TABLES
# =========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    doctor_name VARCHAR(100),
    appointment_date DATE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(100),
    profession VARCHAR(100)
)
""")

db.commit()

# =========================================
# INSERT SAMPLE DOCTORS
# =========================================

cursor.execute("SELECT * FROM doctors")
existing_doctors = cursor.fetchall()

if len(existing_doctors) == 0:

    doctors = [
        ("Dr. Amit Sharma", "Cardiologist"),
        ("Dr. Priya Patil", "Neurologist"),
        ("Dr. Rahul Mehta", "Orthopedic"),
        ("Dr. Sneha Joshi", "Dermatologist"),
        ("Dr. Karan Deshmukh", "General Physician"),
        ("Dr. Neha Kulkarni", "Endocrinologist"),
        ("Dr. Vivek Rao", "Pulmonologist")
    ]

    query = """
    INSERT INTO doctors
    (doctor_name, profession)
    VALUES (%s, %s)
    """

    cursor.executemany(query, doctors)
    db.commit()

# =========================================
# HTML PAGE
# =========================================

HTML_PAGE = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>MediAssist Hospital System</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
rel="stylesheet">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{

    font-family:'Poppins',sans-serif;

    background:
    linear-gradient(
    135deg,
    #0f172a,
    #1e3a8a,
    #2563eb
    );

    min-height:100vh;

    padding:30px;
}

.container{
    max-width:1200px;
    margin:auto;
}

.header{
    text-align:center;
    margin-bottom:30px;
}

.header h1{
    color:white;
    font-size:42px;
}

.header p{
    color:#dbeafe;
    margin-top:10px;
}

.grid{

    display:grid;

    grid-template-columns:
    1fr 1fr;

    gap:25px;
}

.card{

    background:
    rgba(255,255,255,0.12);

    backdrop-filter:blur(15px);

    border-radius:20px;

    padding:25px;

    border:
    1px solid rgba(255,255,255,0.15);

    box-shadow:
    0 8px 25px rgba(0,0,0,0.2);
}

.section-title{

    color:white;

    font-size:22px;

    margin-bottom:20px;
}

input{

    width:100%;

    padding:14px;

    margin-bottom:15px;

    border:none;

    border-radius:12px;

    background:
    rgba(255,255,255,0.15);

    color:white;

    outline:none;

    font-size:15px;
}

input::placeholder{
    color:#d1d5db;
}

button{

    width:100%;

    padding:14px;

    border:none;

    border-radius:12px;

    background:
    linear-gradient(
    135deg,
    #3b82f6,
    #2563eb
    );

    color:white;

    font-size:15px;

    font-weight:600;

    cursor:pointer;

    transition:0.3s;
}

button:hover{

    transform:translateY(-2px);

    box-shadow:
    0 8px 20px rgba(37,99,235,0.5);
}

.doctor-card,
.appointment-card{

    background:
    rgba(255,255,255,0.1);

    padding:15px;

    border-radius:12px;

    margin-bottom:15px;

    color:white;
}

.chat-box{

    height:350px;

    overflow-y:auto;

    background:
    rgba(255,255,255,0.08);

    border-radius:12px;

    padding:15px;

    margin-bottom:15px;
}

.message{

    padding:12px;

    border-radius:10px;

    margin-bottom:10px;

    color:white;

    max-width:85%;

    line-height:1.5;
}

.user{

    background:#2563eb;

    margin-left:auto;

    text-align:right;
}

.bot{

    background:
    rgba(255,255,255,0.15);
}

.chat-input{

    display:flex;

    gap:10px;
}

.chat-input input{
    flex:1;
}

.chat-input button{
    width:100px;
}

.footer{

    text-align:center;

    color:#dbeafe;

    margin-top:30px;
}

.success{

    color:#4ade80;

    margin-top:10px;
}

@media(max-width:900px){

    .grid{
        grid-template-columns:1fr;
    }
}

</style>

</head>

<body>

<div class="container">

    <div class="header">

        <h1>🏥 MediAssist</h1>

        <p>
        Smart Hospital Management System
        </p>

    </div>

    <div class="grid">

        <!-- LEFT -->

        <div>

            <!-- APPOINTMENT SECTION -->

            <div class="card"
            id="appointmentSection"
            style="display:none;">

                <h2 class="section-title">
                📅 Book Appointment
                </h2>

                <form action="/book"
                method="POST">

                    <input type="text"
                    name="patient_name"
                    placeholder="Patient Name"
                    required>

                    <input type="text"
                    name="doctor_name"
                    placeholder="Doctor Name"
                    required>

                    <input type="date"
                    name="appointment_date"
                    required>

                    <button type="submit">
                    Book Appointment
                    </button>

                </form>

            </div>

            <br>

            <!-- CHATBOT -->

            <div class="card">

                <h2 class="section-title">
                🤖 AI Medical Assistant
                </h2>

                <div class="chat-box"
                id="chatBox">

                    <div class="message bot">
                    Hello 👋 Welcome to MediAssist.
                    Ask me about diseases,
                    symptoms, doctors,
                    appointments or emergencies.
                    </div>

                </div>

                <div class="chat-input">

                    <input type="text"
                    id="userInput"
                    placeholder="Ask something...">

                    <button onclick="sendMessage()">
                    Send
                    </button>

                </div>

            </div>

        </div>

        <!-- RIGHT -->

        <div>

            <!-- DOCTORS -->

            <div class="card">

                <h2 class="section-title">
                👨‍⚕️ Available Doctors
                </h2>

                {% for doctor in doctors %}

                <div class="doctor-card">

                    <h3>
                    {{ doctor.doctor_name }}
                    </h3>

                    <p>
                    {{ doctor.profession }}
                    </p>

                </div>

                {% endfor %}

            </div>

            <br>

            <!-- APPOINTMENTS -->

            <div class="card">

                <h2 class="section-title">
                📋 All Appointments
                </h2>

                {% for appointment in appointments %}

                <div class="appointment-card">

                    <h3>
                    {{ appointment.patient_name }}
                    </h3>

                    <p>
                    Doctor:
                    {{ appointment.doctor_name }}
                    </p>

                    <p>
                    Date:
                    {{ appointment.appointment_date }}
                    </p>

                </div>

                {% endfor %}

            </div>

        </div>

    </div>

    <div class="footer">
    © 2026 MediAssist Healthcare
    </div>

</div>

<script>

document.getElementById(
"userInput"
).addEventListener(
"keypress",
function(event){

    if(event.key === "Enter"){

        event.preventDefault();

        sendMessage();
    }
});

async function sendMessage(){

    let input =
    document.getElementById("userInput");

    let message =
    input.value.trim();

    if(message === "") return;

    let chatBox =
    document.getElementById("chatBox");

    // USER MESSAGE

    chatBox.innerHTML +=
    `<div class="message user">
    ${message}
    </div>`;

    input.value = "";

    // FETCH

    let response =
    await fetch("/chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            message:message
        })
    });

    let data =
    await response.json();

    // BOT RESPONSE

    chatBox.innerHTML +=
    `<div class="message bot">
    ${data.response}
    </div>`;

    // SHOW APPOINTMENT FORM

    if(data.showAppointment){

        document.getElementById(
        "appointmentSection"
        ).style.display = "block";

        window.scrollTo({
            top:0,
            behavior:"smooth"
        });
    }

    // AUTO SCROLL

    chatBox.scrollTop =
    chatBox.scrollHeight;
}

</script>

</body>
</html>

"""

# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    cursor.execute(
        "SELECT * FROM doctors"
    )

    doctors = cursor.fetchall()

    cursor.execute("""
    SELECT * FROM appointments
    ORDER BY appointment_id DESC
    """)

    appointments = cursor.fetchall()

    return render_template_string(
        HTML_PAGE,
        doctors=doctors,
        appointments=appointments
    )

# =========================================
# BOOK APPOINTMENT
# =========================================

@app.route("/book", methods=["POST"])
def book():

    patient_name = request.form["patient_name"]

    doctor_name = request.form["doctor_name"]

    appointment_date = request.form["appointment_date"]

    query = """
    INSERT INTO appointments
    (patient_name, doctor_name, appointment_date)
    VALUES (%s,%s,%s)
    """

    values = (
        patient_name,
        doctor_name,
        appointment_date
    )

    cursor.execute(query, values)

    db.commit()

    return """
    <h2>
    Appointment Booked Successfully ✅
    </h2>

    <a href='/'>
    Go Back
    </a>
    """

# =========================================
# CHATBOT
# =========================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data["message"].lower()

    show_appointment = False

    # GREETING

    if "hi" in user_message or "hello" in user_message:

        response = """
        👋 Hello!
        
        I can help with:
        
        • Doctor recommendations
        • Diseases & symptoms
        • Emergency guidance
        • Appointments
        """

    # APPOINTMENT

    elif "appointment" in user_message \
    or "book" in user_message \
    or "consult" in user_message:

        response = """
        📅 Opening appointment section...
        
        Please fill the form above.
        """

        show_appointment = True

    # FEVER

    elif "fever" in user_message:

        response = """
        🤒 Fever detected.
        
        Recommended Doctor:
        👨‍⚕️ General Physician
        
        Drink water and rest properly.
        """

    # CHEST PAIN

    elif "chest pain" in user_message:

        response = """
        ❤️ Chest pain can be serious.
        
        Recommended Doctor:
        👨‍⚕️ Cardiologist
        
        Seek emergency care if severe.
        """

    # DIABETES

    elif "diabetes" in user_message:

        response = """
        🩸 Diabetes specialist:
        
        👨‍⚕️ Endocrinologist
        
        Maintain healthy diet and exercise.
        """

    # SKIN

    elif "skin" in user_message \
    or "pimples" in user_message:

        response = """
        🧴 Recommended Doctor:
        
        👨‍⚕️ Dermatologist
        """

    # HEADACHE

    elif "headache" in user_message:

        response = """
        🧠 Recommended Doctor:
        
        👨‍⚕️ Neurologist
        """

    # EMERGENCY

    elif "emergency" in user_message \
    or "ambulance" in user_message:

        response = """
        🚨 Emergency Number: 102
        
        Please contact nearest hospital immediately.
        """

    # DOCTORS

    elif "doctor" in user_message:

        response = """
        👨‍⚕️ Available Specialists:
        
        • Cardiologist
        • Neurologist
        • Dermatologist
        • Orthopedic
        • Endocrinologist
        • General Physician
        """

    # FALLBACK

    else:

        response = """
        🤖 Sorry,
        I couldn't understand.
        
        Try asking about:
        
        • Fever
        • Diabetes
        • Skin problems
        • Headache
        • Emergency
        • Appointments
        """

    return jsonify({
        "response": response,
        "showAppointment": show_appointment
    })

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":
    app.run(debug=True)