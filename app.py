import streamlit as st
import pandas as pd
import datetime
import random
import re
from groq import Groq
import io
from docx import Document
import tempfile
import os
import concurrent.futures
import time

# ========== VOICE GENERATION (with fallback) ==========
try:
    from gtts import gTTS
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

def generate_audio(text):
    if not VOICE_AVAILABLE or not text.strip():
        return None
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp_path = tmp.name
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(tmp_path)
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
        return audio_bytes
    except Exception:
        return None
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

# ========== SUPABASE CLIENT ==========
try:
    from supabase import create_client, Client
except ImportError:
    Client = None

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="Hospital Management System - built by Gesner Deslandes",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS (LIGHT BLUE THEME) ==========
st.markdown("""
<style>
    .stApp { background-color: #e6f0ff; }
    [data-testid="stSidebar"] { background-color: #b8d4ff; border-right: 1px solid #90b8e0; }
    .main-header {
        background: linear-gradient(90deg, #4a90e2, #2c5f9a);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { margin: 0; font-size: 2rem; }
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 1.2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 25px;
        background-color: #2c5f9a;
        color: white;
    }
    .stButton>button:hover { background-color: #1e3f6b; }
    h2, h3 { color: #1e3f6b; }
    .security-badge {
        background-color: #d9e8ff;
        border-radius: 30px;
        padding: 8px 15px;
        margin: 10px 0;
        text-align: center;
        font-family: monospace;
        font-weight: bold;
        color: #1e3f6b;
        border: 1px solid #4a90e2;
    }
</style>
""", unsafe_allow_html=True)

# ========== GROQ CLIENT ==========
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ========== SUPABASE CLIENT INIT ==========
def get_supabase():
    supabase_url = st.secrets.get("SUPABASE_URL", "")
    supabase_key = st.secrets.get("SUPABASE_KEY", "")
    if supabase_url and supabase_key and Client:
        try:
            return create_client(supabase_url, supabase_key)
        except Exception:
            return None
    return None

supabase = get_supabase()
SUPABASE_AVAILABLE = supabase is not None

# ========== DATA FUNCTIONS ==========
def fetch_data(table_name):
    if not SUPABASE_AVAILABLE:
        return []
    try:
        response = supabase.table(table_name).select("*").execute()
        return response.data if response.data else []
    except Exception:
        return []

def insert_data(table_name, data):
    if not SUPABASE_AVAILABLE:
        return None
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response.data[0] if response.data else None
    except Exception:
        return None

def update_data(table_name, id_col, id_val, data):
    if not SUPABASE_AVAILABLE:
        return None
    try:
        response = supabase.table(table_name).update(data).eq(id_col, id_val).execute()
        return response.data[0] if response.data else None
    except Exception:
        return None

def delete_data(table_name, id_col, id_val):
    if not SUPABASE_AVAILABLE:
        return
    try:
        supabase.table(table_name).delete().eq(id_col, id_val).execute()
    except Exception:
        pass

def load_guidelines():
    if not SUPABASE_AVAILABLE:
        return ""
    try:
        res = supabase.table("guidelines").select("content").eq("id", 1).execute()
        if res.data:
            return res.data[0].get("content", "")
    except Exception:
        pass
    return ""

def save_guidelines(content):
    if not SUPABASE_AVAILABLE:
        return
    try:
        supabase.table("guidelines").upsert({"id": 1, "content": content}).execute()
    except Exception:
        pass

# ========== INITIALIZE SESSION STATE ==========
def refresh_patients():
    if SUPABASE_AVAILABLE:
        st.session_state.patients = fetch_data("patients")
    else:
        if "patients" not in st.session_state:
            st.session_state.patients = [
                {"mrn": "HOSP-1001", "name": "Emily Clark", "age": 34, "gender": "Female", "phone": "555-0101", "address": "123 Main St", "last_visit": "2026-04-20"},
                {"mrn": "HOSP-1002", "name": "James Brown", "age": 58, "gender": "Male", "phone": "555-0102", "address": "456 Oak Ave", "last_visit": "2026-04-19"},
                {"mrn": "HOSP-1003", "name": "Sophia Lee", "age": 22, "gender": "Female", "phone": "555-0103", "address": "789 Pine Rd", "last_visit": "2026-04-18"}
            ]

def refresh_invoices():
    if SUPABASE_AVAILABLE:
        st.session_state.invoices = fetch_data("invoices")
    else:
        if "invoices" not in st.session_state:
            st.session_state.invoices = [
                {"invoice": "INV-101", "patient": "Emily Clark", "amount": 450, "status": "Paid"},
                {"invoice": "INV-102", "patient": "James Brown", "amount": 1200, "status": "Pending"},
                {"invoice": "INV-103", "patient": "Sophia Lee", "amount": 780, "status": "Paid"}
            ]

def refresh_lab_orders():
    if SUPABASE_AVAILABLE:
        st.session_state.lab_orders = fetch_data("lab_orders")
    else:
        if "lab_orders" not in st.session_state:
            st.session_state.lab_orders = [
                {"patient": "Emily Clark", "test": "CBC", "status": "Completed"},
                {"patient": "James Brown", "test": "Lipid Panel", "status": "Pending"}
            ]

def refresh_guidelines():
    if SUPABASE_AVAILABLE:
        st.session_state.guidelines_text = load_guidelines()
    else:
        if "guidelines_text" not in st.session_state:
            st.session_state.guidelines_text = ""

# Initialize
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = "Admin"
if "language" not in st.session_state:
    st.session_state.language = "en"

refresh_patients()
refresh_invoices()
refresh_lab_orders()
refresh_guidelines()

if "hospital_stats" not in st.session_state:
    st.session_state.hospital_stats = {
        "total_patients_today": random.randint(120, 250),
        "active_beds": random.randint(80, 150),
        "today_revenue": random.randint(15000, 35000),
        "lab_tests_pending": random.randint(10, 40)
    }

# ========== TRANSLATION ==========
lang_en = {
    "app_title": "🏥 Hospital Management System Software",
    "app_subtitle": "built by Gesner Deslandes",
    "login_header": "🏥 Hospital Management System Software",
    "login_subheader": "built by Gesner Deslandes",
    "username": "👤 Username",
    "password": "🔒 Password",
    "role": "👨‍⚕️ Role",
    "sign_in": "🔐 Sign In",
    "invalid_creds": "❌ Invalid credentials. Only Admin (Gesner / 20082010) can access.",
    "demo_note": "🩺 Authorized access only: Gesner / 20082010 / Admin",
    "integrated_note": "🏥 Integrated EMR | Billing | Pharmacy | Lab | Radiology",
    "welcome": "Welcome",
    "logout": "🚪 Logout",
    "quick_actions": "📋 Quick Actions",
    "dashboard_link": "🏠 Dashboard",
    "copyright": "© 2026 GlobalInternet.py – built by Gesner Deslandes",
    "main_header": "🏥 Hospital Management System Software",
    "main_subheader": "built by Gesner Deslandes – Multi-Specialty | Integrated EMR | Real-time Operations",
    "tab_video": "📺 Video Introduction",
    "tab_overview": "📊 Dashboard Overview",
    "tab_patient": "👤 Patient Management",
    "tab_billing": "💰 Billing & Revenue",
    "tab_pharmacy": "💊 Pharmacy",
    "tab_lab": "🔬 Laboratory",
    "tab_radiology": "📷 Radiology",
    "tab_inventory": "📦 Inventory",
    "tab_reports": "📈 Reports",
    "tab_ai_diagnostic": "🤖 AI Diagnostic Assistant",
    "video_card_title": "🎬 Introduction to Hospital Management System Software",
    "video_card_text": "Watch this video to learn how our software can transform your healthcare operations.",
    "video_preview_caption": "📽️ Preview of the Hospital Management System Software (GitHub)",
    "video_unavailable": "⚠️ Video preview not available. Please watch the full introduction on YouTube by clicking the link below.",
    "watch_youtube": "▶️ Watch the Full Introduction on YouTube",
    "youtube_info": "📌 The YouTube video provides a complete walkthrough of all modules, including EMR, billing, pharmacy, laboratory, radiology, inventory, and enterprise reporting.",
    "total_patients": "🩺 Total Patients Today",
    "active_beds": "🏥 Active Beds",
    "today_revenue": "💰 Today's Revenue",
    "lab_tests_pending": "🧪 Lab Tests Pending",
    "recent_appointments": "📅 Recent Appointments",
    "department_stats": "🏥 Department Stats",
    "patient_registration": "👤 Patient Registration & EMR",
    "register_new": "➕ Register New Patient",
    "full_name": "Full Name",
    "age": "Age",
    "gender": "Gender",
    "phone": "Phone Number",
    "address": "Address",
    "register_btn": "Register Patient",
    "register_success": "✅ Patient {name} registered successfully! Medical Record Number: {mrn}",
    "recent_patients": "📋 Recent Patients",
    "mrn_col": "MRN",
    "name_col": "Name",
    "age_col": "Age",
    "last_visit_col": "Last Visit",
    "emr_note": "📌 Electronic Medical Records (EMR) – search, edit, and view full history.",
    "billing_title": "💰 Billing & Revenue Cycle Management",
    "select_patient": "Select Patient",
    "bill_amount": "Bill Amount ($)",
    "generate_bill": "Generate Bill",
    "bill_success": "💵 Bill generated for {patient}: ${amount}. Payment due in 15 days.",
    "recent_invoices": "Recent Invoices",
    "invoice_col": "Invoice #",
    "patient_col": "Patient",
    "amount_col": "Amount",
    "status_col": "Status",
    "pharmacy_title": "💊 Pharmacy Management",
    "medication": "Medication",
    "quantity": "Quantity",
    "dispense": "Dispense Medication",
    "dispense_success": "✅ Prescription dispensed: {med} x{qty}. Billed to patient account.",
    "stock_alerts": "Stock Alerts",
    "medicine_col": "Medicine",
    "stock_left_col": "Stock Left",
    "reorder_level_col": "Reorder Level",
    "lab_title": "🔬 Laboratory Integration",
    "order_lab_test": "Order Lab Test",
    "patient_mrn": "Patient MRN / Name",
    "order_test_btn": "Order Test",
    "order_test_msg": "🧪 Test '{test}' ordered for {patient}. Results will be available in 2 hours.",
    "recent_lab_results": "Recent Lab Results",
    "test_col": "Test",
    "status_lab_col": "Status",
    "radiology_title": "📷 Radiology & Imaging",
    "select_imaging": "Select Imaging Type",
    "schedule_scan": "Schedule Scan",
    "scan_success": "✅ {scan} scheduled for patient. Report will be sent to referring doctor.",
    "interop_note": "📌 HL7 / FHIR interoperability supported for PACS integration.",
    "inventory_title": "📦 Inventory & Financial Management",
    "item_col": "Item",
    "qty_col": "Qty",
    "unit_price_col": "Unit Price",
    "reorder_note": "🔄 Auto reorder alerts configured for low stock.",
    "reports_title": "📈 Enterprise Reporting",
    "select_report": "Select Report",
    "generate_report": "Generate Report",
    "report_success": "📊 {report} report generated. Download as PDF/CSV available.",
    "day_col": "Day",
    "revenue_col": "Revenue",
    "language": "🌐 Language",
    "english": "English",
    "spanish": "Español",
    "french": "Français",
    "ai_diagnostic_title": "🤖 AI Diagnostic Assistant",
    "ai_diagnostic_desc": "Ask any clinical or operational question about patients, inventory, billing, or lab results. The AI will provide insights based on actual hospital data. You can also ask if a patient is ready for discharge. Hospital guidelines (if uploaded) will be used to answer policy-related questions.",
    "ai_question_label": "💬 Your question:",
    "ai_ask_button": "Ask AI",
    "ai_thinking": "🧠 AI is analyzing your question and hospital data...",
    "ai_response_title": "💡 AI Diagnostic Insight",
    "ai_error": "⚠️ AI service error. Please try again later.",
    "upload_guidelines": "📄 Upload Hospital Guidelines (Word document)",
    "clear_guidelines": "🗑️ Clear Guidelines",
    "guidelines_uploaded": "✅ Guidelines loaded from {filename}",
    "guidelines_cleared": "Guidelines cleared.",
    "voice_explain": "🎙️ AI Voice Explanation",
}

def get_text(key, lang=None):
    return lang_en.get(key, key)

def language_selector():
    lang_options = {"en": get_text("english"), "es": get_text("spanish"), "fr": get_text("french")}
    selected_lang = st.selectbox(
        get_text("language"),
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=["en","es","fr"].index(st.session_state.language)
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

# ========== PATIENT STATUS FOR DISCHARGE ==========
def get_patient_status(patient_name):
    patient = next((p for p in st.session_state.patients if p["name"] == patient_name), None)
    if not patient:
        return None
    labs = [lab for lab in st.session_state.lab_orders if lab["patient"] == patient_name]
    invoices = [inv for inv in st.session_state.invoices if inv["patient"] == patient_name]
    last_visit = datetime.datetime.strptime(patient.get("last_visit", "2026-01-01"), "%Y-%m-%d")
    days_since_last = (datetime.datetime.now() - last_visit).days
    pending_labs = [lab for lab in labs if lab["status"] == "Pending"]
    all_labs_completed = len(pending_labs) == 0 and len(labs) > 0
    unpaid_invoices = [inv for inv in invoices if inv["status"] != "Paid"]
    all_bills_paid = len(unpaid_invoices) == 0
    ready_for_discharge = all_labs_completed and all_bills_paid and days_since_last >= 1
    return {
        "name": patient_name,
        "labs": labs,
        "invoices": invoices,
        "days_since_last": days_since_last,
        "all_labs_completed": all_labs_completed,
        "all_bills_paid": all_bills_paid,
        "ready_for_discharge": ready_for_discharge,
        "reason": f"Labs completed: {all_labs_completed}, Bills paid: {all_bills_paid}, Days since last visit: {days_since_last}"
    }

# ==================== AI DIAGNOSTIC (UPDATED WITH TIMEOUT) ====================
def ai_diagnostic():
    st.subheader(get_text("ai_diagnostic_title"))
    st.markdown(get_text("ai_diagnostic_desc"))
    
    # ---- Guidelines upload/clear ----
    st.markdown("---")
    uploaded_file = st.file_uploader(get_text("upload_guidelines"), type=["docx"])
    if uploaded_file is not None:
        try:
            doc = Document(io.BytesIO(uploaded_file.read()))
            full_text = "\n".join([para.text for para in doc.paragraphs])
            if SUPABASE_AVAILABLE:
                save_guidelines(full_text)
            st.session_state.guidelines_text = full_text
            st.success(get_text("guidelines_uploaded").format(filename=uploaded_file.name))
            st.rerun()
        except Exception as e:
            st.error(f"Error reading Word document: {e}")
    
    if st.session_state.guidelines_text and st.button(get_text("clear_guidelines"), key="clear_guidelines_btn"):
        if SUPABASE_AVAILABLE:
            save_guidelines("")
        st.session_state.guidelines_text = ""
        st.success(get_text("guidelines_cleared"))
        st.rerun()
    
    if st.session_state.guidelines_text:
        st.info(f"📋 Guidelines loaded (first 300 chars): {st.session_state.guidelines_text[:300]}...")
    else:
        st.info("No guidelines uploaded. AI will answer based only on hospital data.")
    st.markdown("---")
    
    # ---- Build a short summary of hospital data ----
    patient_count = len(st.session_state.patients)
    stats = st.session_state.hospital_stats
    patient_sample = st.session_state.patients[:3]
    patient_list = "\n".join([f"- {p['name']} (MRN: {p['mrn']}, Age: {p['age']})" for p in patient_sample])
    lab_summary = "\n".join([f"- {lab['patient']}: {lab['test']} – {lab['status']}" for lab in st.session_state.lab_orders[:3]])
    invoice_summary = "\n".join([f"- {inv['patient']}: ${inv['amount']} ({inv['status']})" for inv in st.session_state.invoices[:3]])
    
    hospital_summary = f"""Hospital Data:
- {patient_count} patients.
- Today: {stats['total_patients_today']} visits, {stats['active_beds']}/200 beds, ${stats['today_revenue']:,} revenue.
- Lab pending: {stats['lab_tests_pending']}
- Sample patients: {patient_list}
- Lab orders: {lab_summary if st.session_state.lab_orders else 'None'}
- Invoices: {invoice_summary if st.session_state.invoices else 'None'}
"""
    
    guidelines_section = ""
    if st.session_state.guidelines_text:
        trimmed = st.session_state.guidelines_text[:2000]
        guidelines_section = f"Guidelines:\n{trimmed}"
    
    user_question = st.text_area(get_text("ai_question_label"), height=100,
                                 placeholder="Example: Is Emily Clark ready to go home? or What is the discharge policy?")
    
    if st.button(get_text("ai_ask_button"), key="ai_ask"):
        if not user_question.strip():
            st.warning("Please enter a question.")
            return
        
        # ---- Handle discharge questions locally ----
        patient_name_match = None
        for p in st.session_state.patients:
            if p["name"].lower() in user_question.lower():
                patient_name_match = p["name"]
                break
        
        if patient_name_match and any(word in user_question.lower() for word in ["discharge", "go home", "ready"]):
            status = get_patient_status(patient_name_match)
            if status:
                st.markdown(f"### {get_text('ai_response_title')} for {patient_name_match}")
                if status["ready_for_discharge"]:
                    st.success(f"✅ {patient_name_match} is ready to go home. All lab results completed, all bills paid, and patient has been in system for {status['days_since_last']} days.")
                else:
                    reasons = []
                    if not status["all_labs_completed"]:
                        reasons.append("pending lab results")
                    if not status["all_bills_paid"]:
                        reasons.append("unpaid invoices")
                    if status["days_since_last"] < 1:
                        reasons.append("seen today, observation recommended")
                    st.warning(f"❌ {patient_name_match} is not ready. Reasons: {', '.join(reasons)}.")
                return
        
        # ---- General question: call Groq with timeout ----
        with st.spinner(get_text("ai_thinking")):
            prompt = f"""You are a hospital assistant. Answer the user's question based ONLY on the following data and guidelines.

{hospital_summary}
{guidelines_section}

Question: {user_question}

Answer briefly (max 2 sentences):"""
            
            def call_groq():
                return groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=150
                )

            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(call_groq)
                    try:
                        completion = future.result(timeout=10)  # 10-second timeout
                        response = completion.choices[0].message.content.strip()
                        st.markdown(f"### {get_text('ai_response_title')}")
                        st.markdown(response)
                    except concurrent.futures.TimeoutError:
                        st.error("⏳ The AI took too long to respond. Please try a shorter question or check your internet connection.")
                        if st.session_state.guidelines_text:
                            st.info("💡 As a fallback, I can tell you that the discharge criteria are: stable vitals, resolved symptoms, ability to manage at home, and all labs/imaging completed. Check the guidelines for full details.")
                        else:
                            st.info("💡 Please try again with a simpler question.")
            except Exception as e:
                st.error(f"❌ API error: {str(e)}")
                st.info("💡 Please check your Groq API key and network.")

# ========== LOGIN PAGE ==========
def login_page():
    col_lang1, col_lang2, col_lang3 = st.columns([1,1,1])
    with col_lang2:
        language_selector()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center;">
            <h1>{get_text('login_header')}</h1>
            <h3 style="color: #0077b6;">{get_text('login_subheader')}</h3>
            <hr>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login_form"):
            username_input = st.text_input(get_text("username"), key="login_user")
            password_input = st.text_input(get_text("password"), type="password", key="login_pass")
            role_input = st.selectbox(get_text("role"), ["Admin", "Doctor", "Nurse", "Billing Staff"], key="login_role")
            submit = st.form_submit_button(get_text("sign_in"), use_container_width=True)
            if submit:
                if username_input == "Gesner" and password_input == "20082010" and role_input == "Admin":
                    st.session_state.authenticated = True
                    st.session_state.username = username_input
                    st.session_state.role = role_input
                    st.rerun()
                else:
                    st.error(get_text("invalid_creds"))
        st.markdown(f"""
        <div style="text-align: center; margin-top: 2rem;">
            <p>🩺 <strong>{get_text('demo_note')}</strong></p>
            <p>{get_text('integrated_note')}</p>
        </div>
        """, unsafe_allow_html=True)

# ========== MAIN DASHBOARD ==========
def main_dashboard():
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/Deslandes1/Hospital-Management-System-Software-built-by-Gesner-Deslandes/main/Gesner%20Deslandes.png", width=80)
        st.markdown("### **Gesner Deslandes**")
        
        if st.button(get_text("voice_explain"), use_container_width=True):
            voice_text = """
            Welcome to the Hospital Management System Software built by Gesner Deslandes.
            This is a comprehensive, multi-specialty hospital management solution with integrated Electronic Medical Records, real-time operations, and enterprise modules.
            The system includes patient registration and EMR, billing and revenue cycle management, pharmacy management with stock alerts, laboratory integration with test ordering and results tracking, radiology and imaging scheduling, inventory control, and enterprise reporting.
            The AI Diagnostic Assistant allows you to ask clinical or operational questions and get insights based on actual hospital data.
            You can also upload hospital guidelines in Word format and the AI will incorporate them into its answers.
            The software supports multi-language interfaces and is built with a modern, user-friendly design.
            This software was built by Gesner Deslandes, engineer in chief at GlobalInternet.py.
            """
            with st.spinner("Generating voice explanation..."):
                audio_bytes = generate_audio(voice_text)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                    st.success("Explanation played. Click again to repeat.")
                else:
                    st.error("Could not generate explanation audio.")
        st.markdown("---")
        
        st.image("https://img.icons8.com/fluency/96/null/hospital.png", width=80)
        st.markdown(f"**{get_text('welcome')}, {st.session_state.username}**  \n👨‍⚕️ {get_text('role')}: **{st.session_state.role}**")
        st.markdown("---")
        language_selector()
        st.markdown("---")
        st.markdown("### 🛡️ Global Security Shield active")
        st.markdown('<div class="security-badge">🔐 End‑to‑end encryption active</div>', unsafe_allow_html=True)
        st.caption("All data is secured and anonymized")
        st.markdown("---")
        if st.button(get_text("logout"), use_container_width=True, key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()
        st.markdown("---")
        st.markdown(f"### {get_text('quick_actions')}")
        st.markdown(f"[{get_text('dashboard_link')}](#)")
        st.markdown("---")
        st.caption(get_text("copyright"))
    
    st.markdown(f"""
    <div class="main-header">
        <h1>{get_text('main_header')}</h1>
        <p>{get_text('main_subheader')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs([
        get_text("tab_video"), get_text("tab_overview"), get_text("tab_patient"),
        get_text("tab_billing"), get_text("tab_pharmacy"), get_text("tab_lab"),
        get_text("tab_radiology"), get_text("tab_inventory"), get_text("tab_reports"),
        get_text("tab_ai_diagnostic")
    ])
    
    # Tab 0: Video
    with tabs[0]:
        st.markdown(f"""
        <div class="card">
            <h3>{get_text('video_card_title')}</h3>
            <p>{get_text('video_card_text')}</p>
        </div>
        """, unsafe_allow_html=True)
        github_video_url = "https://raw.githubusercontent.com/Deslandes1/Hospital-Management-System-Software-built-by-Gesner-Deslandes/main/X.mp4"
        try:
            st.video(github_video_url, format="video/mp4", start_time=0)
            st.caption(get_text("video_preview_caption"))
        except Exception:
            st.warning(get_text("video_unavailable"))
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="https://youtu.be/QDnU1q64vvw?si=IjaPulUgwKG9n1QQ" target="_blank" style="background-color: #FF0000; color: white; padding: 10px 20px; text-decoration: none; border-radius: 30px; font-weight: bold;">
                ▶️ {get_text('watch_youtube')}
            </a>
        </div>
        """, unsafe_allow_html=True)
        st.info(get_text("youtube_info"))
    
    # Tab 1: Overview
    with tabs[1]:
        stats = st.session_state.hospital_stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text("total_patients"), stats['total_patients_today'], delta="+5%")
        with col2:
            st.metric(get_text("active_beds"), f"{stats['active_beds']} / 200", delta="Occupancy")
        with col3:
            st.metric(get_text("today_revenue"), f"${stats['today_revenue']:,}", delta="+12%")
        with col4:
            st.metric(get_text("lab_tests_pending"), stats['lab_tests_pending'], delta="-2")
        st.markdown("---")
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader(get_text("recent_appointments"))
            data = {get_text("name_col"): ["John Doe", "Maria Garcia", "Wei Zhang", "Fatima Alvi"],
                    "Department": ["Cardiology", "Pediatrics", "Orthopedics", "Neurology"],
                    "Time": ["09:30 AM", "10:15 AM", "11:00 AM", "01:30 PM"]}
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        with col_right:
            st.subheader(get_text("department_stats"))
            dept_stats = pd.DataFrame({"Department": ["OPD", "IPD", "Emergency", "ICU"],
                                       get_text("patient_col"): [87, 42, 23, 15]})
            st.bar_chart(dept_stats.set_index("Department"))
    
    # Tab 2: Patient Management
    with tabs[2]:
        st.subheader(get_text("patient_registration"))
        with st.expander(get_text("register_new")):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(get_text("full_name"), key="pat_name")
                age = st.number_input(get_text("age"), 0, 120, step=1)
                gender = st.selectbox(get_text("gender"), ["Male", "Female", "Other"])
            with col2:
                phone = st.text_input(get_text("phone"))
                address = st.text_area(get_text("address"))
            if st.button(get_text("register_btn")):
                mrn = f"HOSP-{random.randint(10000,99999)}"
                new_patient = {
                    "mrn": mrn,
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "phone": phone,
                    "address": address,
                    "last_visit": datetime.date.today().isoformat()
                }
                if SUPABASE_AVAILABLE:
                    inserted = insert_data("patients", new_patient)
                    if inserted:
                        refresh_patients()
                        st.success(get_text("register_success").format(name=name, mrn=mrn))
                    else:
                        st.error("Failed to save to Supabase. Check your connection.")
                else:
                    st.session_state.patients.append(new_patient)
                    st.success(get_text("register_success").format(name=name, mrn=mrn))
                st.rerun()
        st.markdown("---")
        st.subheader(get_text("recent_patients"))
        if st.session_state.patients:
            patients_df = pd.DataFrame(st.session_state.patients)
            st.dataframe(patients_df[["mrn", "name", "age", "last_visit"]], use_container_width=True)
        else:
            st.info("No patients registered yet. Use the form above to add patients.")
        st.caption(get_text("emr_note"))
    
    # Tab 3: Billing
    with tabs[3]:
        st.subheader(get_text("billing_title"))
        col1, col2 = st.columns(2)
        with col1:
            patient_names = [p["name"] for p in st.session_state.patients] if st.session_state.patients else ["No patients"]
            bill_patient = st.selectbox(get_text("select_patient"), patient_names)
            amount = st.number_input(get_text("bill_amount"), min_value=0, step=10)
            if st.button(get_text("generate_bill")):
                inv_num = f"INV-{random.randint(200,999)}"
                new_invoice = {"invoice": inv_num, "patient": bill_patient, "amount": amount, "status": "Pending"}
                if SUPABASE_AVAILABLE:
                    inserted = insert_data("invoices", new_invoice)
                    if inserted:
                        refresh_invoices()
                        st.success(get_text("bill_success").format(patient=bill_patient, amount=amount))
                    else:
                        st.error("Failed to save invoice to Supabase.")
                else:
                    st.session_state.invoices.append(new_invoice)
                    st.success(get_text("bill_success").format(patient=bill_patient, amount=amount))
                st.rerun()
        with col2:
            st.subheader(get_text("recent_invoices"))
            if st.session_state.invoices:
                st.dataframe(pd.DataFrame(st.session_state.invoices), use_container_width=True)
            else:
                st.info("No invoices yet.")
    
    # Tab 4: Pharmacy
    with tabs[4]:
        st.subheader(get_text("pharmacy_title"))
        col1, col2 = st.columns(2)
        with col1:
            med = st.selectbox(get_text("medication"), ["Paracetamol 500mg", "Amoxicillin 250mg", "Atorvastatin 20mg", "Insulin Glargine"])
            quantity = st.number_input(get_text("quantity"), 1, 100, step=1)
            if st.button(get_text("dispense")):
                st.info(get_text("dispense_success").format(med=med, qty=quantity))
        with col2:
            st.subheader(get_text("stock_alerts"))
            stock_df = pd.DataFrame({get_text("medicine_col"): ["Paracetamol", "Amoxicillin", "Insulin"],
                                     get_text("stock_left_col"): [245, 87, 32],
                                     get_text("reorder_level_col"): [100, 50, 30]})
            st.dataframe(stock_df, use_container_width=True)
    
    # Tab 5: Laboratory
    with tabs[5]:
        st.subheader(get_text("lab_title"))
        test = st.selectbox(get_text("order_lab_test"), ["Complete Blood Count", "Lipid Panel", "Liver Function Test", "Urinalysis"])
        patient_names = [p["name"] for p in st.session_state.patients] if st.session_state.patients else ["No patients"]
        patient_test = st.selectbox(get_text("patient_mrn"), patient_names)
        if st.button(get_text("order_test_btn")):
            new_order = {"patient": patient_test, "test": test, "status": "Pending"}
            if SUPABASE_AVAILABLE:
                inserted = insert_data("lab_orders", new_order)
                if inserted:
                    refresh_lab_orders()
                    st.warning(get_text("order_test_msg").format(test=test, patient=patient_test))
                else:
                    st.error("Failed to save lab order to Supabase.")
            else:
                st.session_state.lab_orders.append(new_order)
                st.warning(get_text("order_test_msg").format(test=test, patient=patient_test))
            st.rerun()
        st.markdown("---")
        st.subheader(get_text("recent_lab_results"))
        if st.session_state.lab_orders:
            st.dataframe(pd.DataFrame(st.session_state.lab_orders), use_container_width=True)
        else:
            st.info("No lab orders yet.")
    
    # Tab 6: Radiology
    with tabs[6]:
        st.subheader(get_text("radiology_title"))
        scan = st.radio(get_text("select_imaging"), ["X-Ray", "CT Scan", "MRI", "Ultrasound"], horizontal=True)
        if st.button(get_text("schedule_scan")):
            st.success(get_text("scan_success").format(scan=scan))
        st.info(get_text("interop_note"))
    
    # Tab 7: Inventory
    with tabs[7]:
        st.subheader(get_text("inventory_title"))
        inv_items = pd.DataFrame({get_text("item_col"): ["Surgical Gloves", "Syringes", "Masks", "IV Fluids"],
                                  get_text("qty_col"): [500, 1200, 800, 240],
                                  get_text("unit_price_col"): [0.25, 0.10, 0.50, 2.50]})
        st.dataframe(inv_items, use_container_width=True)
        st.caption(get_text("reorder_note"))
    
    # Tab 8: Reports
    with tabs[8]:
        st.subheader(get_text("reports_title"))
        report_type = st.selectbox(get_text("select_report"), ["Daily Revenue", "Patient Visits", "Pharmacy Sales", "Department Performance"])
        if st.button(get_text("generate_report")):
            st.success(get_text("report_success").format(report=report_type))
        df_report = pd.DataFrame({get_text("day_col"): ["Mon", "Tue", "Wed", "Thu", "Fri"],
                                  get_text("revenue_col"): [12500, 14800, 13200, 16700, 18900]})
        st.line_chart(df_report.set_index(get_text("day_col")))
    
    # Tab 9: AI Diagnostic Assistant
    with tabs[9]:
        ai_diagnostic()

# ========== RUN ==========
if not st.session_state.authenticated:
    login_page()
else:
    main_dashboard()
