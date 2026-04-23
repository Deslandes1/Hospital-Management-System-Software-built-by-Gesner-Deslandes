import streamlit as st
import pandas as pd
import datetime
import random

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="Hospital Management System - built by Gesner Deslandes",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS FOR ADAPTABLE COLORS & READABILITY ==========
st.markdown("""
<style>
    /* Main background and text */
    .stApp {
        background-color: #f4f7fc;
    }
    .main-header {
        background: linear-gradient(90deg, #0077b6, #023e8a);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
    }
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 1.2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .metric-card {
        text-align: center;
        background: #ffffff;
        border-left: 5px solid #0077b6;
    }
    .logout-btn {
        background-color: #e63946;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        width: 100%;
        cursor: pointer;
        font-weight: bold;
    }
    .logout-btn:hover {
        background-color: #c1121f;
    }
    .stButton>button {
        border-radius: 25px;
        background-color: #0077b6;
        color: white;
    }
    .stButton>button:hover {
        background-color: #023e8a;
    }
    .sidebar .sidebar-content {
        background-color: #e9ecef;
    }
    h2, h3 {
        color: #023e8a;
    }
    hr {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========== INITIALIZE SESSION STATE ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = "Admin"  # default role

# ========== LOGIN PAGE ==========
def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1>🏥 Hospital Management System Software</h1>
            <h3 style="color: #0077b6;">built by Gesner Deslandes</h3>
            <hr>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.text_input("👤 Username", key="login_user")
            st.text_input("🔒 Password", type="password", key="login_pass")
            col_a, col_b = st.columns([1,1])
            with col_a:
                st.selectbox("👨‍⚕️ Role", ["Admin", "Doctor", "Nurse", "Billing Staff"], key="login_role")
            with col_b:
                st.markdown("<br>", unsafe_allow_html=True)  # spacer
            submit = st.form_submit_button("🔐 Sign In", use_container_width=True)
            
            if submit:
                # Simple demo authentication – accept any non-empty username/password
                if st.session_state.login_user and st.session_state.login_pass:
                    st.session_state.authenticated = True
                    st.session_state.username = st.session_state.login_user
                    st.session_state.role = st.session_state.login_role
                    st.rerun()
                else:
                    st.error("❌ Please enter both username and password.")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p>🩺 <strong>Demo credentials:</strong> any username / any password</p>
            <p>🏥 Integrated EMR | Billing | Pharmacy | Lab | Radiology</p>
        </div>
        """, unsafe_allow_html=True)

# ========== MAIN DASHBOARD ==========
def main_dashboard():
    # Sidebar with logout and role info
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/null/hospital.png", width=80)
        st.markdown(f"**Welcome, {st.session_state.username}**  \n👨‍⚕️ Role: **{st.session_state.role}**")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()
        st.markdown("---")
        st.markdown("### 📋 Quick Actions")
        st.page_link("app.py", label="🏠 Dashboard", icon="🏠")
        st.markdown("---")
        st.caption("© 2026 GlobalInternet.py – built by Gesner Deslandes")
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Hospital Management System Software</h1>
        <p>built by Gesner Deslandes – Multi-Specialty | Integrated EMR | Real-time Operations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for core modules
    tabs = st.tabs(["📊 Dashboard Overview", "👤 Patient Management", "💰 Billing & Revenue", "💊 Pharmacy", "🔬 Laboratory", "📷 Radiology", "📦 Inventory", "📈 Reports"])
    
    # ---------- TAB 0: OVERVIEW ----------
    with tabs[0]:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🩺 Total Patients Today", random.randint(120, 250), delta="+5%")
        with col2:
            st.metric("🏥 Active Beds", f"{random.randint(80, 150)} / 200", delta="Occupancy")
        with col3:
            st.metric("💰 Today's Revenue", f"${random.randint(15000, 35000):,}", delta="+12%")
        with col4:
            st.metric("🧪 Lab Tests Pending", random.randint(10, 40), delta="-2")
        
        st.markdown("---")
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("📅 Recent Appointments")
            data = {
                "Patient": ["John Doe", "Maria Garcia", "Wei Zhang", "Fatima Alvi"],
                "Department": ["Cardiology", "Pediatrics", "Orthopedics", "Neurology"],
                "Time": ["09:30 AM", "10:15 AM", "11:00 AM", "01:30 PM"]
            }
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        with col_right:
            st.subheader("🏥 Department Stats")
            dept_stats = pd.DataFrame({
                "Department": ["OPD", "IPD", "Emergency", "ICU"],
                "Patients": [87, 42, 23, 15]
            })
            st.bar_chart(dept_stats.set_index("Department"))
    
    # ---------- TAB 1: PATIENT MANAGEMENT ----------
    with tabs[1]:
        st.subheader("👤 Patient Registration & EMR")
        with st.expander("➕ Register New Patient"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", key="pat_name")
                age = st.number_input("Age", 0, 120, step=1)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            with col2:
                phone = st.text_input("Phone Number")
                address = st.text_area("Address")
            if st.button("Register Patient"):
                st.success(f"✅ Patient {name} registered successfully! Medical Record Number: HOSP-{random.randint(10000,99999)}")
        
        st.markdown("---")
        st.subheader("📋 Recent Patients")
        patients_df = pd.DataFrame({
            "MRN": ["HOSP-1001", "HOSP-1002", "HOSP-1003"],
            "Name": ["Emily Clark", "James Brown", "Sophia Lee"],
            "Age": [34, 58, 22],
            "Last Visit": ["2026-04-20", "2026-04-19", "2026-04-18"]
        })
        st.dataframe(patients_df, use_container_width=True)
        st.caption("📌 Electronic Medical Records (EMR) – search, edit, and view full history.")
    
    # ---------- TAB 2: BILLING ----------
    with tabs[2]:
        st.subheader("💰 Billing & Revenue Cycle Management")
        col1, col2 = st.columns(2)
        with col1:
            bill_patient = st.selectbox("Select Patient", ["Emily Clark (HOSP-1001)", "James Brown (HOSP-1002)", "Sophia Lee (HOSP-1003)"])
            amount = st.number_input("Bill Amount ($)", min_value=0, step=10)
            if st.button("Generate Bill"):
                st.success(f"💵 Bill generated for {bill_patient}: ${amount}. Payment due in 15 days.")
        with col2:
            st.subheader("Recent Invoices")
            inv_data = {
                "Invoice #": ["INV-101", "INV-102", "INV-103"],
                "Patient": ["Emily Clark", "James Brown", "Sophia Lee"],
                "Amount": [450, 1200, 780],
                "Status": ["Paid", "Pending", "Paid"]
            }
            st.dataframe(pd.DataFrame(inv_data), use_container_width=True)
    
    # ---------- TAB 3: PHARMACY ----------
    with tabs[3]:
        st.subheader("💊 Pharmacy Management")
        col1, col2 = st.columns(2)
        with col1:
            med = st.selectbox("Medication", ["Paracetamol 500mg", "Amoxicillin 250mg", "Atorvastatin 20mg", "Insulin Glargine"])
            quantity = st.number_input("Quantity", 1, 100, step=1)
            if st.button("Dispense Medication"):
                st.info(f"✅ Prescription dispensed: {med} x{quantity}. Billed to patient account.")
        with col2:
            st.subheader("Stock Alerts")
            stock_df = pd.DataFrame({
                "Medicine": ["Paracetamol", "Amoxicillin", "Insulin"],
                "Stock Left": [245, 87, 32],
                "Reorder Level": [100, 50, 30]
            })
            st.dataframe(stock_df, use_container_width=True)
    
    # ---------- TAB 4: LABORATORY ----------
    with tabs[4]:
        st.subheader("🔬 Laboratory Integration")
        test = st.selectbox("Order Lab Test", ["Complete Blood Count", "Lipid Panel", "Liver Function Test", "Urinalysis"])
        patient_test = st.text_input("Patient MRN / Name", "HOSP-1001")
        if st.button("Order Test"):
            st.warning(f"🧪 Test '{test}' ordered for {patient_test}. Results will be available in 2 hours.")
        
        st.markdown("---")
        st.subheader("Recent Lab Results")
        lab_data = {
            "Patient": ["Emily Clark", "James Brown"],
            "Test": ["CBC", "Lipid Panel"],
            "Status": ["Completed", "Pending"]
        }
        st.dataframe(pd.DataFrame(lab_data), use_container_width=True)
    
    # ---------- TAB 5: RADIOLOGY ----------
    with tabs[5]:
        st.subheader("📷 Radiology & Imaging")
        scan = st.radio("Select Imaging Type", ["X-Ray", "CT Scan", "MRI", "Ultrasound"], horizontal=True)
        if st.button("Schedule Scan"):
            st.success(f"✅ {scan} scheduled for patient. Report will be sent to referring doctor.")
        st.info("📌 HL7 / FHIR interoperability supported for PACS integration.")
    
    # ---------- TAB 6: INVENTORY ----------
    with tabs[6]:
        st.subheader("📦 Inventory & Financial Management")
        inv_items = pd.DataFrame({
            "Item": ["Surgical Gloves", "Syringes", "Masks", "IV Fluids"],
            "Qty": [500, 1200, 800, 240],
            "Unit Price": [0.25, 0.10, 0.50, 2.50]
        })
        st.dataframe(inv_items, use_container_width=True)
        st.caption("🔄 Auto reorder alerts configured for low stock.")
    
    # ---------- TAB 7: REPORTS ----------
    with tabs[7]:
        st.subheader("📈 Enterprise Reporting")
        report_type = st.selectbox("Select Report", ["Daily Revenue", "Patient Visits", "Pharmacy Sales", "Department Performance"])
        if st.button("Generate Report"):
            st.success(f"📊 {report_type} report generated. Download as PDF/CSV available.")
        # Sample chart
        df_report = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
            "Revenue": [12500, 14800, 13200, 16700, 18900]
        })
        st.line_chart(df_report.set_index("Day"))

# ========== APP ROUTING ==========
if not st.session_state.authenticated:
    login_page()
else:
    main_dashboard()
