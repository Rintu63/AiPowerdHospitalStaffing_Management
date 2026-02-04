![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-purple?logo=pandas)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-AI-orange)
![Google Colab](https://img.shields.io/badge/Google%20Colab-Notebook-orange?logo=googlecolab)
![VS Code](https://img.shields.io/badge/VS%20Code-IDE-blue?logo=visualstudiocode)
![Healthcare AI](https://img.shields.io/badge/Healthcare-AI-green)

🏥 AI-Based Hospital Staffing & Operations Optimization System
📌 Overview

This project is an AI-driven Hospital Staffing and Operations Decision Support System designed to assist healthcare administrators in making data-driven staffing decisions under normal, proactive, and emergency conditions. The system analyzes real-time hospital operational data and provides intelligent insights to improve patient care, reduce caregiver burnout, and enhance overall hospital efficiency.

🩺 Problem Statement

Hospitals face significant challenges in managing staff efficiently due to fluctuating patient loads, emergency situations, staff shortages, and caregiver fatigue. Traditional manual staffing approaches lack real-time intelligence and often result in overcrowding, delayed treatment, and operational inefficiencies. There is a need for an intelligent system that can support proactive and emergency staffing decisions using real-time data and analytics.

💡 Solution Approach

The system uses a combination of machine learning models and a rule-based risk assessment engine to evaluate hospital operational conditions. Based on real-time inputs such as patient load, ICU and emergency occupancy, staff availability, and external risk factors, the system classifies hospital conditions into:

Normal Mode

Proactive Mode

Emergency Mode

It then supports staffing decisions, triggers emergency alerts for doctors, and logs operational data for historical analysis.

✨ Key Features

AI-based hospital staffing decision support

Real-time patient load and risk assessment

Emergency alert triggering for doctors

Automatic staff ID generation and staff management

Interactive dashboard with risk indicators

Historical analytics (daily, weekly, monthly, yearly trends)

Audit logging for transparency and traceability

🏗️ System Architecture

Flow:
Data Collection → AI & Risk Assessment → Decision Engine → Emergency Alerts → Data Storage → Dashboard Visualization

The architecture is modular and scalable, enabling easy integration with future enhancements.

🛠️ Technology Stack

Programming Language: Python

Frontend / Dashboard: Streamlit

Backend Framework: Flask

AI & Analytics: Machine Learning models, Rule-based risk engine

Data Handling: Pandas

Data Storage: CSV files

Development Tools: VS Code, Git

📊 Dashboard Screens (Examples)

Hospital staffing overview dashboard

Risk level and emergency alert display

Staff management (Add / View Staff)

Analytics and historical trends

(Screenshots can be added here)

🎯 Outcomes & Learning

Developed a real-world AI-based healthcare decision support system

Gained hands-on experience in AI, data analytics, and system design

Improved understanding of hospital operations and emergency response planning

Enhanced skills in Python programming, dashboard development, and documentation

🚀 Future Scope

Integration with SMS/Email/WhatsApp alert systems

Advanced predictive analytics for staffing forecasts

Role-based access control

Integration with hospital information systems (EHR/HMS)

Cloud deployment and mobile application support

📁 Project Structure
AI-Hospital-Staffing-System/
│
├── backend/
│   └── app.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── staff_schedule.csv
│   ├── daily_snapshot.csv
│   └── audit_log.csv
│
├── README.md

▶️ How to Run the Project (Optional)

Clone the repository

Install required Python packages

Run the backend:

python backend/app.py


Run the dashboard:

streamlit run dashboard/app.py

📄 License

This project is developed for educational and internship purposes under the AICTE Internship Program.

👤 Author

Lalatendu Kumar Sahu
B.Tech – Computer Science and Engineering
