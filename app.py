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

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

# ========== INITIALIZE SESSION STATE ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = "Admin"
if "language" not in st.session_state:
    st.session_state.language = "en"  # default English

# ========== TRANSLATION DICTIONARIES ==========
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
    "french": "Français"
}

lang_es = {
    "app_title": "🏥 Sistema de Gestión Hospitalaria",
    "app_subtitle": "construido por Gesner Deslandes",
    "login_header": "🏥 Sistema de Gestión Hospitalaria",
    "login_subheader": "construido por Gesner Deslandes",
    "username": "👤 Usuario",
    "password": "🔒 Contraseña",
    "role": "👨‍⚕️ Rol",
    "sign_in": "🔐 Iniciar Sesión",
    "invalid_creds": "❌ Credenciales inválidas. Solo Admin (Gesner / 20082010) puede acceder.",
    "demo_note": "🩺 Acceso autorizado únicamente: Gesner / 20082010 / Admin",
    "integrated_note": "🏥 EMR integrado | Facturación | Farmacia | Laboratorio | Radiología",
    "welcome": "Bienvenido",
    "logout": "🚪 Cerrar Sesión",
    "quick_actions": "📋 Acciones Rápidas",
    "dashboard_link": "🏠 Panel",
    "copyright": "© 2026 GlobalInternet.py – construido por Gesner Deslandes",
    "main_header": "🏥 Sistema de Gestión Hospitalaria",
    "main_subheader": "construido por Gesner Deslandes – Multi-especialidad | EMR integrado | Operaciones en tiempo real",
    "tab_video": "📺 Introducción en Video",
    "tab_overview": "📊 Resumen del Panel",
    "tab_patient": "👤 Gestión de Pacientes",
    "tab_billing": "💰 Facturación e Ingresos",
    "tab_pharmacy": "💊 Farmacia",
    "tab_lab": "🔬 Laboratorio",
    "tab_radiology": "📷 Radiología",
    "tab_inventory": "📦 Inventario",
    "tab_reports": "📈 Informes",
    "video_card_title": "🎬 Introducción al Sistema de Gestión Hospitalaria",
    "video_card_text": "Mire este video para aprender cómo nuestro software puede transformar sus operaciones sanitarias.",
    "video_preview_caption": "📽️ Vista previa del Sistema de Gestión Hospitalaria (GitHub)",
    "video_unavailable": "⚠️ Vista previa no disponible. Mire la introducción completa en YouTube haciendo clic en el enlace.",
    "watch_youtube": "▶️ Ver Introducción Completa en YouTube",
    "youtube_info": "📌 El video de YouTube ofrece un recorrido completo de todos los módulos, incluyendo EMR, facturación, farmacia, laboratorio, radiología, inventario e informes empresariales.",
    "total_patients": "🩺 Pacientes Hoy",
    "active_beds": "🏥 Camas Activas",
    "today_revenue": "💰 Ingresos Hoy",
    "lab_tests_pending": "🧪 Pruebas de Laboratorio Pendientes",
    "recent_appointments": "📅 Citas Recientes",
    "department_stats": "🏥 Estadísticas por Departamento",
    "patient_registration": "👤 Registro de Pacientes y EMR",
    "register_new": "➕ Registrar Nuevo Paciente",
    "full_name": "Nombre Completo",
    "age": "Edad",
    "gender": "Género",
    "phone": "Teléfono",
    "address": "Dirección",
    "register_btn": "Registrar Paciente",
    "register_success": "✅ Paciente {name} registrado exitosamente. Número de Historia: {mrn}",
    "recent_patients": "📋 Pacientes Recientes",
    "mrn_col": "Nº Historia",
    "name_col": "Nombre",
    "age_col": "Edad",
    "last_visit_col": "Última Visita",
    "emr_note": "📌 Registros Médicos Electrónicos (EMR) – buscar, editar y ver historial completo.",
    "billing_title": "💰 Facturación y Gestión del Ciclo de Ingresos",
    "select_patient": "Seleccionar Paciente",
    "bill_amount": "Monto de Factura ($)",
    "generate_bill": "Generar Factura",
    "bill_success": "💵 Factura generada para {patient}: ${amount}. Pago en 15 días.",
    "recent_invoices": "Facturas Recientes",
    "invoice_col": "Factura #",
    "patient_col": "Paciente",
    "amount_col": "Monto",
    "status_col": "Estado",
    "pharmacy_title": "💊 Gestión de Farmacia",
    "medication": "Medicamento",
    "quantity": "Cantidad",
    "dispense": "Dispensar Medicamento",
    "dispense_success": "✅ Prescripción dispensada: {med} x{qty}. Facturada a la cuenta del paciente.",
    "stock_alerts": "Alertas de Inventario",
    "medicine_col": "Medicamento",
    "stock_left_col": "Stock Restante",
    "reorder_level_col": "Nivel de Reorden",
    "lab_title": "🔬 Integración de Laboratorio",
    "order_lab_test": "Solicitar Prueba de Laboratorio",
    "patient_mrn": "Nº Historia / Nombre del Paciente",
    "order_test_btn": "Solicitar Prueba",
    "order_test_msg": "🧪 Prueba '{test}' solicitada para {patient}. Resultados en 2 horas.",
    "recent_lab_results": "Resultados de Laboratorio Recientes",
    "test_col": "Prueba",
    "status_lab_col": "Estado",
    "radiology_title": "📷 Radiología e Imágenes",
    "select_imaging": "Seleccionar Tipo de Imagen",
    "schedule_scan": "Programar Estudio",
    "scan_success": "✅ {scan} programado para el paciente. Informe enviado al médico.",
    "interop_note": "📌 Interoperabilidad HL7 / FHIR compatible con integración PACS.",
    "inventory_title": "📦 Gestión de Inventario y Finanzas",
    "item_col": "Artículo",
    "qty_col": "Cantidad",
    "unit_price_col": "Precio Unitario",
    "reorder_note": "🔄 Alertas de reorden automáticas configuradas para stock bajo.",
    "reports_title": "📈 Informes Empresariales",
    "select_report": "Seleccionar Informe",
    "generate_report": "Generar Informe",
    "report_success": "📊 Informe {report} generado. Disponible para descargar en PDF/CSV.",
    "day_col": "Día",
    "revenue_col": "Ingresos",
    "language": "🌐 Idioma",
    "english": "Inglés",
    "spanish": "Español",
    "french": "Francés"
}

lang_fr = {
    "app_title": "🏥 Logiciel de Gestion Hospitalière",
    "app_subtitle": "construit par Gesner Deslandes",
    "login_header": "🏥 Logiciel de Gestion Hospitalière",
    "login_subheader": "construit par Gesner Deslandes",
    "username": "👤 Nom d'utilisateur",
    "password": "🔒 Mot de passe",
    "role": "👨‍⚕️ Rôle",
    "sign_in": "🔐 Se connecter",
    "invalid_creds": "❌ Identifiants invalides. Seul l'Admin (Gesner / 20082010) peut accéder.",
    "demo_note": "🩺 Accès autorisé uniquement : Gesner / 20082010 / Admin",
    "integrated_note": "🏥 DME intégré | Facturation | Pharmacie | Laboratoire | Radiologie",
    "welcome": "Bienvenue",
    "logout": "🚪 Déconnexion",
    "quick_actions": "📋 Actions rapides",
    "dashboard_link": "🏠 Tableau de bord",
    "copyright": "© 2026 GlobalInternet.py – construit par Gesner Deslandes",
    "main_header": "🏥 Logiciel de Gestion Hospitalière",
    "main_subheader": "construit par Gesner Deslandes – Multi-spécialités | DME intégré | Opérations en temps réel",
    "tab_video": "📺 Introduction vidéo",
    "tab_overview": "📊 Aperçu du tableau de bord",
    "tab_patient": "👤 Gestion des patients",
    "tab_billing": "💰 Facturation et revenus",
    "tab_pharmacy": "💊 Pharmacie",
    "tab_lab": "🔬 Laboratoire",
    "tab_radiology": "📷 Radiologie",
    "tab_inventory": "📦 Inventaire",
    "tab_reports": "📈 Rapports",
    "video_card_title": "🎬 Introduction au logiciel de gestion hospitalière",
    "video_card_text": "Regardez cette vidéo pour découvrir comment notre logiciel peut transformer vos opérations de santé.",
    "video_preview_caption": "📽️ Aperçu du logiciel de gestion hospitalière (GitHub)",
    "video_unavailable": "⚠️ Aperçu vidéo non disponible. Veuillez regarder l'introduction complète sur YouTube en cliquant sur le lien ci-dessous.",
    "watch_youtube": "▶️ Regarder l'introduction complète sur YouTube",
    "youtube_info": "📌 La vidéo YouTube fournit un aperçu complet de tous les modules, y compris DME, facturation, pharmacie, laboratoire, radiologie, inventaire et rapports d'entreprise.",
    "total_patients": "🩺 Patients aujourd'hui",
    "active_beds": "🏥 Lits actifs",
    "today_revenue": "💰 Recettes du jour",
    "lab_tests_pending": "🧪 Tests de laboratoire en attente",
    "recent_appointments": "📅 Rendez-vous récents",
    "department_stats": "🏥 Statistiques par département",
    "patient_registration": "👤 Enregistrement des patients et DME",
    "register_new": "➕ Enregistrer un nouveau patient",
    "full_name": "Nom complet",
    "age": "Âge",
    "gender": "Genre",
    "phone": "Numéro de téléphone",
    "address": "Adresse",
    "register_btn": "Enregistrer le patient",
    "register_success": "✅ Patient {name} enregistré avec succès. Numéro de dossier : {mrn}",
    "recent_patients": "📋 Patients récents",
    "mrn_col": "N° Dossier",
    "name_col": "Nom",
    "age_col": "Âge",
    "last_visit_col": "Dernière visite",
    "emr_note": "📌 Dossiers médicaux électroniques (DME) – rechercher, modifier et voir l'historique complet.",
    "billing_title": "💰 Facturation et gestion du cycle de revenus",
    "select_patient": "Sélectionner un patient",
    "bill_amount": "Montant de la facture ($)",
    "generate_bill": "Générer la facture",
    "bill_success": "💵 Facture générée pour {patient} : ${amount}. Paiement dû dans 15 jours.",
    "recent_invoices": "Factures récentes",
    "invoice_col": "Facture n°",
    "patient_col": "Patient",
    "amount_col": "Montant",
    "status_col": "Statut",
    "pharmacy_title": "💊 Gestion de la pharmacie",
    "medication": "Médicament",
    "quantity": "Quantité",
    "dispense": "Délivrer le médicament",
    "dispense_success": "✅ Prescription délivrée : {med} x{qty}. Facturé au compte du patient.",
    "stock_alerts": "Alertes de stock",
    "medicine_col": "Médicament",
    "stock_left_col": "Stock restant",
    "reorder_level_col": "Niveau de réapprovisionnement",
    "lab_title": "🔬 Intégration du laboratoire",
    "order_lab_test": "Prescrire un test de laboratoire",
    "patient_mrn": "N° dossier / Nom du patient",
    "order_test_btn": "Prescrire le test",
    "order_test_msg": "🧪 Test '{test}' prescrit pour {patient}. Résultats disponibles dans 2 heures.",
    "recent_lab_results": "Résultats de laboratoire récents",
    "test_col": "Test",
    "status_lab_col": "Statut",
    "radiology_title": "📷 Radiologie et imagerie",
    "select_imaging": "Sélectionner le type d'imagerie",
    "schedule_scan": "Planifier l'examen",
    "scan_success": "✅ {scan} planifié pour le patient. Rapport envoyé au médecin référent.",
    "interop_note": "📌 Interopérabilité HL7 / FHIR prise en charge pour l'intégration PACS.",
    "inventory_title": "📦 Gestion des stocks et des finances",
    "item_col": "Article",
    "qty_col": "Qté",
    "unit_price_col": "Prix unitaire",
    "reorder_note": "🔄 Alertes de réapprovisionnement automatique configurées pour les stocks faibles.",
    "reports_title": "📈 Rapports d'entreprise",
    "select_report": "Sélectionner un rapport",
    "generate_report": "Générer le rapport",
    "report_success": "📊 Rapport {report} généré. Téléchargement PDF/CSV disponible.",
    "day_col": "Jour",
    "revenue_col": "Revenus",
    "language": "🌐 Langue",
    "english": "Anglais",
    "spanish": "Espagnol",
    "french": "Français"
}

def get_text(key, lang=None):
    if lang is None:
        lang = st.session_state.language
    if lang == "es":
        return lang_es.get(key, key)
    elif lang == "fr":
        return lang_fr.get(key, key)
    else:
        return lang_en.get(key, key)

# ========== LANGUAGE SELECTOR COMPONENT ==========
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

# ========== LOGIN PAGE ==========
def login_page():
    # Language selector at top
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
    # Sidebar with logout and language selector
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/null/hospital.png", width=80)
        st.markdown(f"**{get_text('welcome')}, {st.session_state.username}**  \n👨‍⚕️ {get_text('role')}: **{st.session_state.role}**")
        st.markdown("---")
        language_selector()
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
    
    # Main header
    st.markdown(f"""
    <div class="main-header">
        <h1>{get_text('main_header')}</h1>
        <p>{get_text('main_subheader')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tabs = st.tabs([
        get_text("tab_video"),
        get_text("tab_overview"),
        get_text("tab_patient"),
        get_text("tab_billing"),
        get_text("tab_pharmacy"),
        get_text("tab_lab"),
        get_text("tab_radiology"),
        get_text("tab_inventory"),
        get_text("tab_reports")
    ])
    
    # ---------- TAB 0: VIDEO INTRODUCTION ----------
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
        except Exception as e:
            st.warning(get_text("video_unavailable"))
        
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="https://youtu.be/QDnU1q64vvw?si=IjaPulUgwKG9n1QQ" target="_blank" style="background-color: #FF0000; color: white; padding: 10px 20px; text-decoration: none; border-radius: 30px; font-weight: bold;">
                ▶️ {get_text('watch_youtube')}
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(get_text("youtube_info"))
    
    # ---------- TAB 1: OVERVIEW ----------
    with tabs[1]:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text("total_patients"), random.randint(120, 250), delta="+5%")
        with col2:
            st.metric(get_text("active_beds"), f"{random.randint(80, 150)} / 200", delta="Occupancy")
        with col3:
            st.metric(get_text("today_revenue"), f"${random.randint(15000, 35000):,}", delta="+12%")
        with col4:
            st.metric(get_text("lab_tests_pending"), random.randint(10, 40), delta="-2")
        
        st.markdown("---")
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader(get_text("recent_appointments"))
            data = {
                get_text("name_col"): ["John Doe", "Maria Garcia", "Wei Zhang", "Fatima Alvi"],
                "Department": ["Cardiology", "Pediatrics", "Orthopedics", "Neurology"],
                "Time": ["09:30 AM", "10:15 AM", "11:00 AM", "01:30 PM"]
            }
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        with col_right:
            st.subheader(get_text("department_stats"))
            dept_stats = pd.DataFrame({
                "Department": ["OPD", "IPD", "Emergency", "ICU"],
                get_text("patient_col"): [87, 42, 23, 15]
            })
            st.bar_chart(dept_stats.set_index("Department"))
    
    # ---------- TAB 2: PATIENT MANAGEMENT ----------
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
                st.success(get_text("register_success").format(name=name, mrn=mrn))
        
        st.markdown("---")
        st.subheader(get_text("recent_patients"))
        patients_df = pd.DataFrame({
            get_text("mrn_col"): ["HOSP-1001", "HOSP-1002", "HOSP-1003"],
            get_text("name_col"): ["Emily Clark", "James Brown", "Sophia Lee"],
            get_text("age_col"): [34, 58, 22],
            get_text("last_visit_col"): ["2026-04-20", "2026-04-19", "2026-04-18"]
        })
        st.dataframe(patients_df, use_container_width=True)
        st.caption(get_text("emr_note"))
    
    # ---------- TAB 3: BILLING ----------
    with tabs[3]:
        st.subheader(get_text("billing_title"))
        col1, col2 = st.columns(2)
        with col1:
            bill_patient = st.selectbox(get_text("select_patient"), ["Emily Clark (HOSP-1001)", "James Brown (HOSP-1002)", "Sophia Lee (HOSP-1003)"])
            amount = st.number_input(get_text("bill_amount"), min_value=0, step=10)
            if st.button(get_text("generate_bill")):
                st.success(get_text("bill_success").format(patient=bill_patient, amount=amount))
        with col2:
            st.subheader(get_text("recent_invoices"))
            inv_data = {
                get_text("invoice_col"): ["INV-101", "INV-102", "INV-103"],
                get_text("patient_col"): ["Emily Clark", "James Brown", "Sophia Lee"],
                get_text("amount_col"): [450, 1200, 780],
                get_text("status_col"): ["Paid", "Pending", "Paid"]
            }
            st.dataframe(pd.DataFrame(inv_data), use_container_width=True)
    
    # ---------- TAB 4: PHARMACY ----------
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
            stock_df = pd.DataFrame({
                get_text("medicine_col"): ["Paracetamol", "Amoxicillin", "Insulin"],
                get_text("stock_left_col"): [245, 87, 32],
                get_text("reorder_level_col"): [100, 50, 30]
            })
            st.dataframe(stock_df, use_container_width=True)
    
    # ---------- TAB 5: LABORATORY ----------
    with tabs[5]:
        st.subheader(get_text("lab_title"))
        test = st.selectbox(get_text("order_lab_test"), ["Complete Blood Count", "Lipid Panel", "Liver Function Test", "Urinalysis"])
        patient_test = st.text_input(get_text("patient_mrn"), "HOSP-1001")
        if st.button(get_text("order_test_btn")):
            st.warning(get_text("order_test_msg").format(test=test, patient=patient_test))
        
        st.markdown("---")
        st.subheader(get_text("recent_lab_results"))
        lab_data = {
            get_text("name_col"): ["Emily Clark", "James Brown"],
            get_text("test_col"): ["CBC", "Lipid Panel"],
            get_text("status_lab_col"): ["Completed", "Pending"]
        }
        st.dataframe(pd.DataFrame(lab_data), use_container_width=True)
    
    # ---------- TAB 6: RADIOLOGY ----------
    with tabs[6]:
        st.subheader(get_text("radiology_title"))
        scan = st.radio(get_text("select_imaging"), ["X-Ray", "CT Scan", "MRI", "Ultrasound"], horizontal=True)
        if st.button(get_text("schedule_scan")):
            st.success(get_text("scan_success").format(scan=scan))
        st.info(get_text("interop_note"))
    
    # ---------- TAB 7: INVENTORY ----------
    with tabs[7]:
        st.subheader(get_text("inventory_title"))
        inv_items = pd.DataFrame({
            get_text("item_col"): ["Surgical Gloves", "Syringes", "Masks", "IV Fluids"],
            get_text("qty_col"): [500, 1200, 800, 240],
            get_text("unit_price_col"): [0.25, 0.10, 0.50, 2.50]
        })
        st.dataframe(inv_items, use_container_width=True)
        st.caption(get_text("reorder_note"))
    
    # ---------- TAB 8: REPORTS ----------
    with tabs[8]:
        st.subheader(get_text("reports_title"))
        report_type = st.selectbox(get_text("select_report"), ["Daily Revenue", "Patient Visits", "Pharmacy Sales", "Department Performance"])
        if st.button(get_text("generate_report")):
            st.success(get_text("report_success").format(report=report_type))
        df_report = pd.DataFrame({
            get_text("day_col"): ["Mon", "Tue", "Wed", "Thu", "Fri"],
            get_text("revenue_col"): [12500, 14800, 13200, 16700, 18900]
        })
        st.line_chart(df_report.set_index(get_text("day_col")))

# ========== APP ROUTING ==========
if not st.session_state.authenticated:
    login_page()
else:
    main_dashboard()
