import streamlit as st
import requests
import json
import os
from datetime import date
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="OnboardAI",
    page_icon="🤖",
    layout="wide"
)

# =========================
# Styling
# =========================

st.markdown("""
<style>

.stApp{
    background-color:#0E1117;
}

[data-testid="stSidebar"]{
    background-color:#111827;
}

div[data-testid="metric-container"]{
    background-color:#1F2937;
    padding:20px;
    border-radius:15px;
    border:1px solid #374151;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:45px;
    font-weight:bold;
}

.stTextInput input{
    border-radius:10px;
}

.stSelectbox div{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Login
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown("""
    # 🤖 OnboardAI 

    ### AI Powered Employee Onboarding Platform """)

    st.markdown("---")

    username = st.text_input("Username / Email")
    password = st.text_input("Password", type="password")

    remember = st.checkbox("Remember Me")

    login_btn = st.button("🔐 Login")

    if login_btn:

        if username == "vishnu" and password == "vishnu123":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    
    if st.button("🔑 Forgot Password"):
        st.success("A password reset link has been sent.")
    
    st.stop()


# =========================
# Data Setup
# =========================
FILES = [
    "employees.json","candidates.json","offer_letters.json",
    "attendance.json","leaves.json","performance.json",
    "payroll.json","exit.json","experience_letters.json"
]

if not os.path.exists("data"):
    os.makedirs("data")

for file in FILES:
    path = f"data/{file}"
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)

def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

employees = load_data("data/employees.json")
candidates = load_data("data/candidates.json")
offers = load_data("data/offer_letters.json")
attendance = load_data("data/attendance.json")
leaves = load_data("data/leaves.json")
performance = load_data("data/performance.json")
payroll = load_data("data/payroll.json")
exit_records = load_data("data/exit.json")
experience_letters = load_data("data/experience_letters.json")

employee_names = [emp["name"] for emp in employees]

# =========================
# Sidebar Branding
# =========================

with st.sidebar:
    st.markdown("## 🤖 OnboardAI HRMS")   # ✅ Branding line at top
    st.markdown("---")                    # Divider

    # Sidebar menu
    menu = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👨‍💼 Hiring",
            "📄 Offer Letter",
            "📝 Employee Registration",
            "💰 Payroll Management",
            "📅 Attendance Management",
            "🏖️ Leave Management",
            "📈 Performance Management",
            "🚪 Exit Management",
            "📜 Experience Letter",
            "📊 HR Analytics",
            "👥 Employee Directory",
            "🚀 Onboarding Center"
        ],
        key="menu"
    )

# Logout option
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", key="logout_btn"):
    st.session_state.clear()
    st.sidebar.success("You have been logged out.")
    st.stop()
# =========================
# Dashboard (single screen layout)
# =========================


def show_dashboard():
    # Header row: Title (left) + Welcome (right)
    col_title, col_welcome = st.columns([2,2])

    with col_title:
        st.markdown("## 🤖 OnboardAI HRMS Dashboard")

    with col_welcome:
        if "username" in st.session_state:
            st.markdown(f"### 👋 Welcome back, **{st.session_state.username}**!")
        else:
            st.markdown("### 👋 Welcome back!")

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("👥 Employees", len(employees))
    with c2: st.metric("👨‍💼 Candidates", len(candidates))
    with c3: st.metric("📄 Offers", len(offers))
    with c4: st.metric("📅 Attendance Today", len(attendance))

    st.markdown("---")

    # Main row: 3 columns
    col1, col2, col3 = st.columns([1.5,1,1])

    # Column 1: Hiring Panel (longer)
    with col1:
        st.markdown("### 👨‍💼 Hiring Panel")
        candidate_name = st.text_input("Candidate Name", key="cand_name_dashboard")
        candidate_email = st.text_input("Candidate Email", key="cand_email_dashboard")
        candidate_experience = st.number_input("Experience (yrs)", min_value=0, max_value=20, value=1, key="cand_exp_dashboard")
        candidate_skill = st.selectbox("Skill", ["Python","Java","SQL","ML"], key="cand_skill_dashboard")
        if st.button("Add Candidate", key="add_cand_btn_dashboard"):
            candidate_id = f"CAN{len(candidates)+1:03d}"
            candidates.append({
                "candidate_id": candidate_id,
                "name": candidate_name,
                "email": candidate_email,
                "experience": candidate_experience,
                "skill": candidate_skill,
                "status": "Applied"
            })
            with open("data/candidates.json","w") as f: json.dump(candidates,f,indent=4)
            st.success("Candidate Added")

    # Column 2: Candidate Records (top) + HR Analytics (bottom)
    with col2:
        st.markdown("### 📋 Candidate Records")
        if len(candidates) > 0:
            st.dataframe(candidates, width=600, height=160)
        else:
            st.info("No candidates")

        st.markdown("### 📊 HR Analytics")
        data = {
            "Category": ["Employees","Candidates","Offers","Attendance"],
            "Count": [len(employees), len(candidates), len(offers), len(attendance)]
        }
        fig = px.pie(data, values="Count", names="Category", width=260, height=260)
        st.plotly_chart(fig, use_container_width=False)

    # Column 3: AI Score (top) + Employee Directory (bottom)
    with col3:
        st.markdown("### 🤖 AI Candidate Score")
        if len(candidates) > 0:
            selected_candidate = st.selectbox("Select Candidate",[c["name"] for c in candidates], key="cand_score_select_dashboard")
            st.success("AI Score: 85 / 100")
            st.write("Strong Hire")
        else:
            st.info("No candidates")

        st.markdown("### 👥 Employee Directory")
        if len(employees) > 0:
            st.dataframe(employees, width=600, height=160)
        else:
            st.info("No employees")

    st.markdown("---")

    # ✅ Onboarding Panel integrated here
    st.markdown("### 🚀 Start Onboarding")

    role = st.selectbox("Select Role", ["Software Engineer", "Data Scientist"], key="onboard_role")
    plan = {}
    if st.button("Generate Onboarding Plan", key="onboard_btn"):
        with open("config/onboarding.json") as f:
            rules = json.load(f)
        plan = rules.get(role, {})

        # Show plan as table with grouped items per category
        if plan:
            steps = []
            for section, items in plan.items():
                steps.append({"Category": section.capitalize(), "Items": ", ".join(items)})
            df = pd.DataFrame(steps)
            st.dataframe(df, width=600, height=250)
        else:
            st.warning("No onboarding plan found for this role.")

    # Run onboarding simulation
    if plan and st.button("Run Onboarding", key="run_onboard"):
        user = st.session_state.get("username", "New Employee")
        for acc in plan.get("accounts", []):
            st.write(f"✅ Created {acc} account for {user}")
        for cloud in plan.get("cloud_access", []):
            st.write(f"☁️ Provisioned {cloud} for {user}")
        for tool in plan.get("tools", []):
            st.write(f"🛠 Installed {tool} for {user}")
        for course in plan.get("training", []):
            st.write(f"📚 Assigned {course} to {user}")
        for storage in plan.get("storage", []):
            st.write(f"💾 Setup {storage} for {user}")
        st.success("🎉 Onboarding Completed")

# Run dashboard only when selected
if menu == "🏠 Dashboard":
    show_dashboard()

# =========================
# Hiring Module
# =========================

def show_hiring():
    # Header row: Title (left) + Welcome (right)
    col_title, col_welcome = st.columns([2,2])

    with col_title:
        st.markdown("## 👨‍💼 Hiring Module")

    with col_welcome:
        if "username" in st.session_state:
            st.markdown(f"### 👋 Welcome, **{st.session_state.username}**!")
        else:
            st.markdown("### 👋 Welcome!")

    st.markdown("---")

    # Candidate Form
    st.markdown("### ➕ Add New Candidate")
    cand_name = st.text_input("Candidate Name", key="cand_name_hiring")
    cand_email = st.text_input("Candidate Email", key="cand_email_hiring")
    cand_exp = st.number_input("Experience (yrs)", min_value=0, max_value=20, value=1, key="cand_exp_hiring")
    cand_skill = st.selectbox("Skill", ["Python","Java","SQL","ML"], key="cand_skill_hiring")

    if st.button("Add Candidate", key="add_cand_btn_hiring"):
        cand_id = f"CAN{len(candidates)+1:03d}"
        new_cand = {
            "candidate_id": cand_id,
            "name": cand_name,
            "email": cand_email,
            "experience": cand_exp,
            "skill": cand_skill,
            "status": "Applied"
        }
        candidates.append(new_cand)
        with open("data/candidates.json","w") as f:
            json.dump(candidates,f,indent=4)
        st.success(f"Candidate {cand_name} added successfully!")

    st.markdown("---")

    # Candidate Records Table (show all details)
    st.markdown("### 📋 Candidate Records")
    if len(candidates) > 0:
        df = pd.DataFrame(candidates)  # full details: ID, name, email, experience, skill, status
        st.dataframe(df, width=800, height=250)
    else:
        st.info("No candidates yet.")

    st.markdown("---")

    # ✅ AI Candidate Score Section
    st.markdown("### 🤖 AI Candidate Score")
    if len(candidates) > 0:
        selected_candidate = st.selectbox(
            "Select Candidate",
            [c["name"] for c in candidates],
            key="cand_score_select_hiring"
        )
        cand = next(c for c in candidates if c["name"] == selected_candidate)
        # Safe access: make sure 'experience' exists
        exp = cand.get("experience", 0)
        score = min(100, exp * 10 + 50)  # simple formula
        st.success(f"AI Score: {score} / 100")
        if score >= 80:
            st.write("Strong Hire")
        elif score >= 60:
            st.write("Potential Hire")
        else:
            st.write("Needs Improvement")
    else:
        st.info("No candidates available for scoring.")

    st.markdown("---")

    # Footer
    st.caption("OnboardAI HRMS © 2026 All Rights Reserved")


# Run hiring module only when selected
if menu == "👨‍💼 Hiring":
    show_hiring()


from fpdf import FPDF
import os

# =========================
# Offer Letter Module
# =========================

def show_offer_letter():
    # Header row
    col_title, col_welcome = st.columns([2,2])
    with col_title:
        st.markdown("## 📄 Offer Letter Module")
    with col_welcome:
        if "username" in st.session_state:
            st.markdown(f"### 👋 Welcome, **{st.session_state.username}**!")
        else:
            st.markdown("### 👋 Welcome!")

    st.markdown("---")

    # Offer Letter Form
    st.markdown("### ➕ Generate Offer Letter")
    cand_name = st.text_input("Candidate Name", key="offer_cand_name")
    cand_address = st.text_area("Candidate Address", key="offer_cand_address")
    job_title = st.text_input("Job Title", key="offer_job_title")
    department = st.text_input("Department", key="offer_department")
    manager_name = st.text_input("Reporting Manager", key="offer_manager")
    location = st.text_input("Work Location", key="offer_location")
    joining_date = st.date_input("Joining Date", key="offer_joining_date")
    ctc = st.number_input("Annual CTC (INR)", min_value=0, step=1000, key="offer_ctc")
    ctc_words = st.text_input("CTC in Words", key="offer_ctc_words")
    probation = st.selectbox("Probation Period", ["3 months","6 months"], key="offer_probation")
    notice_period = st.selectbox("Notice Period", ["30 days","60 days","90 days"], key="offer_notice")

    if st.button("Create Offer Letter", key="create_offer_btn"):
        offer_id = f"OFR{len(offers)+1:03d}"

        # Generate formatted letter text (compact, no acceptance part)
        offer_text = f"""
OFFER LETTER

Date: {joining_date.strftime('%d/%m/%Y')}

To,
{cand_name}
{cand_address}

Subject: Offer of Employment

Dear {cand_name},

We are pleased to offer you the position of {job_title} at OnboardAI HRMS.

EMPLOYMENT DETAILS
Employee Name      : {cand_name}
Designation        : {job_title}
Department         : {department}
Reporting Manager  : {manager_name}
Work Location      : {location}
Joining Date       : {joining_date.strftime('%d/%m/%Y')}
Employment Type    : Full-Time

COMPENSATION
Your annual Cost to Company (CTC) will be INR {ctc} (Rupees {ctc_words} Only) per annum.

PROBATION
You will be on probation for {probation}. Confirmation will follow satisfactory completion.

WORKING HOURS
Standard working hours and leave entitlements as per company policy.

CONFIDENTIALITY
You must maintain confidentiality of all company information during and after employment.

TERMINATION
Either party may terminate employment with {notice_period} notice or salary in lieu thereof.

We are delighted to welcome you to OnboardAI HRMS and look forward to a successful professional relationship.

Sincerely,
HR Department
OnboardAI HRMS
"""

        # ✅ Create PDF (single page, compact)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 6, offer_text.strip())
        os.makedirs("generated_offers", exist_ok=True)
        pdf_path = f"generated_offers/{offer_id}_{cand_name}.pdf"
        pdf.output(pdf_path)

        new_offer = {
            "offer_id": offer_id,
            "candidate": cand_name,
            "position": job_title,
            "salary": ctc,
            "status": "Generated",
            "letter": offer_text.strip(),
            "pdf_path": pdf_path
        }
        offers.append(new_offer)

        # Save to JSON
        with open("data/offers.json","w") as f:
            json.dump(offers,f,indent=4)

        st.success(f"Offer Letter for {cand_name} created successfully!")
        st.text_area("Generated Offer Letter", offer_text.strip(), height=400)

    st.markdown("---")

    # Offer Records Table with Download
    st.markdown("### 📋 Offer Letters")
    if len(offers) > 0:
        for offer in offers:
            st.write(f"**{offer['offer_id']} - {offer['candidate']} ({offer['position']}) - INR {offer['salary']}**")
            st.write(f"Status: {offer['status']}")
            st.download_button(
                label="⬇️ Download Offer Letter (PDF)",
                data=open(offer["pdf_path"], "rb").read(),
                file_name=os.path.basename(offer["pdf_path"]),
                mime="application/pdf",
                key=f"download_{offer['offer_id']}"
            )
            st.markdown("---")
    else:
        st.info("No offers yet.")

    st.markdown("---")

    # Footer
    st.caption("OnboardAI HRMS © 2026 All Rights Reserved")


# Run offer letter module only when selected
if menu == "📄 Offer Letter":
    show_offer_letter()

# =========================
# Employee Registration
# =========================
def show_employee_registration():
    st.header("📝 Employee Registration")

    emp_name = st.text_input("Employee Name")
    emp_email = st.text_input("Employee Email")
    emp_dept = st.text_input("Department")
    emp_role = st.text_input("Role / Designation")
    emp_join_date = st.date_input("Joining Date")

    if st.button("Register Employee"):
        emp_id = f"EMP{len(employees)+1:03d}"
        new_emp = {
            "employee_id": emp_id,
            "name": emp_name,
            "email": emp_email,
            "department": emp_dept,
            "role": emp_role,
            "joining_date": str(emp_join_date)
        }
        employees.append(new_emp)
        with open("data/employees.json","w") as f:
            json.dump(employees,f,indent=4)
        st.success(f"Employee {emp_name} registered successfully!")

    st.subheader("Employee Records")
    if employees:
        st.dataframe(employees, use_container_width=True)
    else:
        st.info("No employees registered yet.")

# Run employee registration module only when selected
if menu == "📝 Employee Registration":
    show_employee_registration()

# =========================
# Payroll Management
# =========================
def show_payroll_management():
    st.header("💰 Payroll Management")

    if employee_names:
        payroll_employee = st.selectbox("Employee", employee_names)
        salary = st.number_input("Monthly Salary", min_value=10000, value=30000)
        month = st.text_input("Month", value="June 2026")
        status = st.selectbox("Status", ["Pending", "Paid"])

        if st.button("Generate Payroll"):
            payroll_record = {
                "employee": payroll_employee,
                "salary": salary,
                "month": month,
                "status": status
            }
            payroll.append(payroll_record)
            with open("data/payroll.json","w") as f:
                json.dump(payroll,f,indent=4)
            st.success(f"Payroll generated for {payroll_employee} ({month})")

    st.subheader("Payroll Records")
    if payroll:
        st.dataframe(payroll, use_container_width=True)
    else:
        st.info("No payroll records")

# Run payroll module only when selected
if menu == "💰 Payroll Management":
    show_payroll_management()


# =========================
# Attendance Management
# =========================
def show_attendance_management():
    st.header("📅 Attendance Management")

    if employee_names:
        attendance_employee = st.selectbox("Employee", employee_names)
        attendance_status = st.selectbox("Status", ["Present", "Absent"])
        if st.button("Mark Attendance"):
            attendance.append({
                "employee": attendance_employee,
                "date": str(date.today()),
                "status": attendance_status
            })
            with open("data/attendance.json","w") as f:
                json.dump(attendance,f,indent=4)
            st.success("Attendance Marked")

    st.subheader("Attendance Records")
    if attendance:
        st.dataframe(attendance, use_container_width=True)
    else:
        st.info("No attendance records")

# Run attendance module only when selected
if menu == "📅 Attendance Management":
    show_attendance_management()


# =========================
# Leave Management
# =========================
def show_leave_management():
    st.header("🏖️ Leave Management")

    if employee_names:
        leave_employee = st.selectbox("Employee Name", employee_names)
        leave_type = st.selectbox("Leave Type", ["Casual Leave", "Sick Leave", "Earned Leave"])
        if st.button("Apply Leave"):
            leave_record = {
                "employee": leave_employee,
                "leave_type": leave_type,
                "status": "Approved"
            }
            leaves.append(leave_record)
            with open("data/leaves.json","w") as f:
                json.dump(leaves,f,indent=4)
            st.success(f"Leave approved for {leave_employee}")

    st.subheader("Leave Records")
    if leaves:
        st.dataframe(leaves, use_container_width=True)
    else:
        st.info("No leave records")

# Run leave module only when selected
if menu == "🏖️ Leave Management":
    show_leave_management()

# =========================
# Performance Management
# =========================
def show_performance_management():
    st.header("📈 Performance Management")

    if employee_names:
        perf_employee = st.selectbox("Employee", employee_names)
        rating = st.slider("Performance Rating", 1, 5, 3)
        if st.button("Save Rating"):
            perf_record = {
                "employee": perf_employee,
                "rating": rating
            }
            performance.append(perf_record)
            with open("data/performance.json","w") as f:
                json.dump(performance,f,indent=4)
            st.success(f"Performance rating saved for {perf_employee}")

    st.subheader("Performance Records")
    if performance:
        st.dataframe(performance, use_container_width=True)
    else:
        st.info("No performance records")

# Run performance module only when selected
if menu == "📈 Performance Management":
    show_performance_management()

# =========================
# Exit Management
# =========================
def show_exit_management():
    st.header("🚪 Exit Management")

    if employee_names:
        exit_employee = st.selectbox("Employee Leaving", employee_names)
        reason = st.text_input("Exit Reason")
        if st.button("Process Exit"):
            exit_record = {
                "employee": exit_employee,
                "reason": reason,
                "date": str(date.today())
            }
            exit_records.append(exit_record)
            with open("data/exit.json","w") as f:
                json.dump(exit_records,f,indent=4)
            st.success(f"Exit processed for {exit_employee}")

    st.subheader("Exit Records")
    if exit_records:
        st.dataframe(exit_records, use_container_width=True)
    else:
        st.info("No exit records")

# Run exit module only when selected
if menu == "🚪 Exit Management":
    show_exit_management()

# =========================
# Experience Letter Module
# =========================
def show_experience_letter():
    st.header("📜 Experience Letter")

    emp_name = st.text_input("Employee Name")
    emp_address = st.text_area("Employee Address")
    designation = st.text_input("Designation")
    department = st.text_input("Department")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    manager_name = st.text_input("Reporting Manager")
    location = st.text_input("Work Location")

    if st.button("Create Experience Letter"):
        if not emp_name or not designation or not department:
            st.error("Please fill all required fields.")
            return

        exp_id = f"EXP{len(experience_letters)+1:03d}"

        exp_text = f"""
EXPERIENCE LETTER

Date: {end_date.strftime('%d/%m/%Y')}

To,
{emp_name}
{emp_address}

Subject: Experience Certificate

Dear {emp_name},

This is to certify that {emp_name} was employed with OnboardAI HRMS as {designation} in the {department} department from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}.

During this period, {emp_name} reported to {manager_name} and was based at our {location} office. We found {emp_name} to be sincere, hardworking, and dedicated to their responsibilities.

We wish {emp_name} all the best in future endeavors.

Sincerely,
HR Department
OnboardAI HRMS
"""

        # ✅ Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, exp_text.strip())
        os.makedirs("generated_experience", exist_ok=True)
        pdf_path = f"generated_experience/{exp_id}_{emp_name}.pdf"
        pdf.output(pdf_path)

        new_exp = {
            "exp_id": exp_id,
            "employee": emp_name,
            "designation": designation,
            "department": department,
            "status": "Generated",
            "letter": exp_text.strip(),
            "pdf_path": pdf_path
        }
        experience_letters.append(new_exp)
        with open("data/experience_letters.json","w") as f:
            json.dump(experience_letters,f,indent=4)

        st.success(f"Experience Letter for {emp_name} created successfully!")
        st.text_area("Generated Experience Letter", exp_text.strip(), height=400)

    st.subheader("📋 Experience Letters")
    if experience_letters:
        for exp in experience_letters:
            st.write(f"**{exp['exp_id']} - {exp['employee']} ({exp['designation']}) - {exp['department']}**")
            st.download_button(
                "⬇️ Download Experience Letter (PDF)",
                open(exp["pdf_path"], "rb").read(),
                file_name=os.path.basename(exp["pdf_path"]),
                mime="application/pdf"
            )
            st.markdown("---")
    else:
        st.info("No experience letters yet.")

    st.caption("OnboardAI HRMS © 2026 All Rights Reserved")

# Run experience letter module only when selected
if menu == "📜 Experience Letter":
    show_experience_letter()


# =========================
# HR Analytics
# =========================
def show_hr_analytics():
    st.header("📊 HR Analytics")

    # Metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", len(employees))
    col2.metric("Total Candidates", len(candidates))
    col3.metric("Total Leaves", len(leaves))

    # Example chart: Performance ratings distribution
    if performance:
        perf_df = pd.DataFrame(performance)
        fig = px.histogram(perf_df, x="rating", nbins=5, title="Performance Ratings Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # Example chart: Payroll status
    if payroll:
        payroll_df = pd.DataFrame(payroll)
        fig2 = px.pie(payroll_df, names="status", title="Payroll Status")
        st.plotly_chart(fig2, use_container_width=True)

    st.caption("OnboardAI HRMS © 2026 All Rights Reserved")

# Run HR Analytics module only when selected
if menu == "📊 HR Analytics":
    show_hr_analytics()

# =========================
# Employee Directory
# =========================
def show_employee_directory():
    st.header("👥 Employee Directory")

    if employees:
        st.dataframe(employees, use_container_width=True)
    else:
        st.info("No employees found")

# Run employee directory module only when selected
if menu == "👥 Employee Directory":
    show_employee_directory()

# =========================
# Onboarding Center
# =========================
def show_onboarding_center():

    st.header("🚀 Employee Onboarding Center")

    if not employees:
        st.warning("No employees available.")
        return

    employee_names = [emp["name"] for emp in employees]

    # Employee Selection
    selected_employee = st.selectbox(
        "Select Employee",
        employee_names,
        key="onboarding_employee"
    )

    # Onboarding Progress
    personal_details = st.checkbox(
        "Personal Details Submitted",
        key="personal_details"
    )

    documents_uploaded = st.checkbox(
        "Documents Uploaded",
        key="documents_uploaded"
    )

    background_check = st.checkbox(
        "Background Verification",
        key="background_check"
    )

    training_completed = st.checkbox(
        "Training Completed",
        key="training_completed"
    )

    manager_approval = st.checkbox(
        "Manager Approval",
        key="manager_approval"
    )

    completed = sum([
        personal_details,
        documents_uploaded,
        background_check,
        training_completed,
        manager_approval
    ])

    progress = int((completed / 5) * 100)

    st.progress(progress)

    st.success(
        f"Onboarding Progress: {progress}%"
    )

    st.subheader("Current Status")

    if progress == 100:
        st.success("✅ Employee Fully Onboarded")
    else:
        st.warning("⏳ Onboarding In Progress")

    # Personal Details Section
    st.subheader("👤 Personal Details")

    full_name = st.text_input(
        "Full Name",
        key="full_name"
    )

    father_name = st.text_input(
        "Father Name",
        key="father_name"
    )

    dob = st.date_input(
        "Date of Birth",
        key="dob"
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        key="gender"
    )

    phone = st.text_input(
        "Mobile Number",
        key="phone"
    )

    email = st.text_input(
        "Email",
        key="email"
    )

    address = st.text_area(
        "Address",
        key="address"
    )

    emergency_contact = st.text_input(
        "Emergency Contact Number",
        key="emergency_contact"
    )

    blood_group = st.selectbox(
        "Blood Group",
        [
            "A+", "A-",
            "B+", "B-",
            "O+", "O-",
            "AB+", "AB-"
        ],
        key="blood_group"
    )

    # File Uploads
    resume = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"],
        key="resume_upload"
    )

    id_proof = st.file_uploader(
    "🪪 Upload Aadhaar Card",
    type=["pdf", "png", "jpg", "jpeg"],
    key="aadhaar_upload"
    )

    pan_card = st.file_uploader(
    "💳 Upload PAN Card",
    type=["pdf", "png", "jpg", "jpeg"],
    key="pan_upload"
    )

    photo = st.file_uploader(
    "📸 Upload Employee Photo",
    type=["png", "jpg", "jpeg"],
    key="photo_upload"
    )

    if photo:
        st.image(photo, width=200)

    st.subheader("🤖 AI Verification Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
     if resume:
        st.success("✅ Resume Uploaded")

    with col2:
     if id_proof:
        st.success("✅ Aadhaar Uploaded")

    with col3:
     if pan_card:
        st.success("✅ PAN Uploaded")

    with col4:
     if photo:
        st.success("✅ Employee Photo Uploaded")
    
    if st.button(
        "📋 Generate Report",
        key="generate_report"
    ):
        st.success("Onboarding Report Generated")

    # Document Verification
    st.header("📄 Document Verification")

    verification_employee = st.selectbox(
        "Select Employee for Verification",
        employee_names,
        key="verification_employee"
    )

    resume_verified = st.checkbox(
        "Resume Verified",
        key="resume_verified"
    )

    aadhaar_verified = st.checkbox(
        "Aadhaar Verified",
        key="aadhaar_verified"
    )

    pan_verified = st.checkbox(
        "PAN Verified",
        key="pan_verified"
    )

    photo_verified = st.checkbox(
        "Photo Verified",
        key="photo_verified"
    )

    if (
        resume_verified and
        aadhaar_verified and
        pan_verified and
        photo_verified
    ):
        st.success("✅ Employee Verified")
    else:
        st.warning("⏳ Verification Pending")
if menu == "🚀 Onboarding Center":
    show_onboarding_center()

st.markdown("---")

st.caption(
    "© 2026 OnboardAI | Employee Onboarding System"
)