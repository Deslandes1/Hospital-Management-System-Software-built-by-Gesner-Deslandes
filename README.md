# 🏥 Hospital Management System Software

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Made with Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Groq AI](https://img.shields.io/badge/Groq-LLM-purple.svg)](https://groq.com)

**Built by Gesner Deslandes, Engineer‑in‑Chief at GlobalInternet.py**

A comprehensive, AI‑powered hospital management system with integrated EMR, billing, pharmacy, laboratory, radiology, inventory, and an intelligent diagnostic assistant that answers clinical and operational questions using real‑time hospital data and uploaded policy guidelines.

🔗 **Live Demo:** [Your Streamlit App URL]

---

## ✨ Features

### Core Modules
| Module | Description |
|--------|-------------|
| 📺 **Video Introduction** | Walkthrough video explaining all features. |
| 📊 **Dashboard Overview** | Real‑time metrics: total patients, active beds, revenue, lab tests pending. |
| 👤 **Patient Management & EMR** | Register patients, store medical records, view recent patients. |
| 💰 **Billing & Revenue** | Generate invoices, track payments, view revenue reports. |
| 💊 **Pharmacy** | Dispense medications, monitor stock alerts. |
| 🔬 **Laboratory** | Order lab tests, track results. |
| 📷 **Radiology** | Schedule X‑Ray, CT, MRI, Ultrasound. |
| 📦 **Inventory** | Manage medical supplies, auto‑reorder alerts. |
| 📈 **Reports** | Daily revenue, patient visits, department performance. |
| 🤖 **AI Diagnostic Assistant** | Ask questions about patients, labs, billing, inventory, or hospital policies. AI uses actual hospital data and uploaded Word documents to give accurate, context‑aware answers. Also checks patient readiness for discharge based on lab completion, bill payment, and length of stay. |

### AI Capabilities
- **Discharge readiness check** – The AI evaluates if a patient is ready to go home (labs completed, bills paid, observation period satisfied).
- **Policy‑aware answers** – Upload hospital guidelines (`.docx`) and the AI will answer based on your official protocols.
- **Real‑time data integration** – All answers are grounded in the actual hospital data stored in the system (patient list, lab orders, invoices, etc.). No hallucinated numbers.

### Technical Highlights
- 🛡️ **Global Security Shield** – End‑to‑end encryption badge (API key never exposed).
- 🌐 **Multilingual UI** – English, Spanish, French (easily extensible).
- 🧠 **Generative AI** – Powered by Groq Llama 3.1 (fast, free inference).
- 🔗 **HL7 / FHIR ready** – Designed for interoperability with PACS, lab systems, and EHRs.

---

## 🛠️ Tech Stack

- **Frontend & Deployment**: [Streamlit](https://streamlit.io)
- **AI Model**: [Groq](https://groq.com) – Llama 3.1 8B
- **Word Document Parsing**: `python-docx`
- **Data Handling**: Pandas, Python datetime
- **Language**: Python 3.12

---

## 📦 Installation (Local Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Deslandes1/hospital-management-system.git
   cd hospital-management-system
