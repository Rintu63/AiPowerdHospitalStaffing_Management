"""
AI-Powered Urban Hospital Staffing System
Backend API (Single Control Panel)

Responsibilities:
- Predict patient load (ML model)
- Calculate department-wise staff requirements
- Check real-time staff availability
- Select staff for emergency & normal operations
- Trigger AI automation (alerts + shift updates)
"""

# --------------------------------------------------
# 1. IMPORTS
# --------------------------------------------------
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
from datetime import date

# Project modules
from config import MODEL_PATH, STAFF_DATA_PATH
from scheduler import load_staff, classify_staff
from staffing_rules import staff_requirements
from emergency import select_staff

from automation_agent import HospitalStaffingAgent

# Ensure data directory exists
os.makedirs("data", exist_ok=True)


def calculate_risk_score(payload):
    """
    Calculate overall hospital operational risk (0–100)
    """

    score = 0

    # -----------------------------
    # Patient severity
    # -----------------------------
    severity = payload.get("severity_mix", {})
    score += severity.get("critical", 0) * 0.4
    score += severity.get("moderate", 0) * 0.2

    # -----------------------------
    # Occupancy pressure
    # -----------------------------
    occupancy = payload.get("occupancy", {})
    score += occupancy.get("icu", 0) * 0.3
    score += occupancy.get("er", 0) * 0.2

    # -----------------------------
    # Staff pressure
    # -----------------------------
    staff_pressure = payload.get("staff_pressure", {})
    score += staff_pressure.get("fatigued_pct", 0) * 0.3

    if staff_pressure.get("transport_issue") == "Yes":
        score += 10

    # -----------------------------
    # Time context
    # -----------------------------
    time_ctx = payload.get("time_context", {})
    if time_ctx.get("shift") == "Night":
        score += 10
    if time_ctx.get("special_day") != "Normal Day":
        score += 10

    # -----------------------------
    # External risk
    # -----------------------------
    external = payload.get("external_risk")
    if external == "Weather Alert":
        score += 10
    elif external == "Accident Nearby":
        score += 15
    elif external == "Disease Outbreak":
        score += 25

    return min(int(score), 100)

SNAPSHOT_PATH = os.path.join("data", "daily_snapshot.csv")
def save_daily_snapshot(payload, staff_df):
    today = date.today().isoformat()

    doctors = len(staff_df[staff_df["role"] == "Doctor"])
    nurses = len(staff_df[staff_df["role"] == "Nurse"])
    sisters = len(staff_df[staff_df["role"] == "Sister"])

    snapshot = {
        "date": today,
        "doctors": doctors,
        "nurses": nurses,
        "sisters": sisters,
        "patients_opd": payload["opd_patients"],
        "patients_emergency": payload["emergency_patients"],
        "patients_icu": payload["icu_patients"]
    }

    if os.path.exists(SNAPSHOT_PATH):
        df = pd.read_csv(SNAPSHOT_PATH)
        if today not in df["date"].astype(str).values:
            df = pd.concat([df, pd.DataFrame([snapshot])], ignore_index=True)
    else:
        df = pd.DataFrame([snapshot])

    df.to_csv(SNAPSHOT_PATH, index=False)

# --------------------------------------------------
# 2. APP INITIALIZATION
# --------------------------------------------------
app = Flask(__name__)

# Load trained ML model
model = joblib.load(MODEL_PATH)

# Initialize AI Automation Agent
automation_agent = HospitalStaffingAgent(model)


# --------------------------------------------------
# 3. HEALTH CHECK ENDPOINT
# --------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    """
    Simple health check for monitoring
    """
    return jsonify({
        "status": "running",
        "service": "Urban Hospital AI Staffing Backend"
    })


# --------------------------------------------------
# 4. MAIN AI STAFFING ENDPOINT
# --------------------------------------------------
@app.route("/urban_ai_staffing", methods=["POST"])
def urban_ai_staffing():
    """
    Main AI endpoint for hospital staffing decisions
    """

    # ------------------------------
    # 4.1 Read Input Data
    # ------------------------------
    data = request.json
    # -----------------------------
    # AI Risk Assessment
    # -----------------------------
    risk_score = calculate_risk_score(data)

    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    required_fields = [
        "opd_patients",
        "emergency_patients",
        "icu_patients",
        "available_nurses",
        "available_doctors"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # ------------------------------
    # 4.2 Demand Prediction (ML)
    # ------------------------------
    X = pd.DataFrame([{
        "opd_patients": data["opd_patients"],
        "emergency_patients": data["emergency_patients"],
        "icu_patients": data["icu_patients"],
        "available_nurses": data["available_nurses"],
        "available_doctors": data["available_doctors"]
    }])

    predicted_patients = int(model.predict(X)[0])

    # ------------------------------
    # 4.3 Load & Classify Staff
    # ------------------------------
    staff_df = load_staff(STAFF_DATA_PATH)

    on_duty, off_duty_ready, blocked = classify_staff(staff_df)

    # ------------------------------
    # 4.4 Department-wise Staff Needs
    # ------------------------------
    requirement_rules = staff_requirements(predicted_patients)

    staffing_plan = {}

    for department, roles in requirement_rules.items():
        staffing_plan[department] = {}

        for role, count in roles.items():
            selected_staff = select_staff(
                on_duty_df=on_duty,
                off_duty_df=off_duty_ready,
                role=role,
                department=department,
                count=count
            )

            staffing_plan[department][role] = selected_staff

    # ------------------------------
    # 4.5 AI Automation Decision
    # ------------------------------
    situation = automation_agent.assess_situation(predicted_patients)

    updated_staff_df, automation_logs = automation_agent.execute(
        situation=situation,
        staffing_plan=staffing_plan,
        staff_df=staff_df
    )

    # ------------------------------
    # 4.6 Final Structured Response
    # ------------------------------
    response = {
        "risk_assessment": {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "explanation": (
            "Risk is computed using patient severity, department occupancy, "
            "staff fatigue, time context, and external signals.")
        },

        "patient_prediction": {
            "predicted_total_patients": predicted_patients,
            "decision_mode": situation
        },
        "staffing_plan": staffing_plan,
        "staff_status_summary": {
            "on_duty_count": len(on_duty),
            "off_duty_ready_count": len(off_duty_ready),
            "blocked_staff_count": len(blocked)
        },
        "ai_automation": {
            "automation_level": "Semi-Autonomous (Human-in-the-loop)",
            "actions_taken": automation_logs
        },
        "explainability": {
            "why_fast_decision": (
                "AI already knows staff-to-patient ratios and real-time "
                "availability, so it performs direct selection instead of "
                "manual reasoning."
            ),
            "safety_measures": [
                "Burnout filtering",
                "Leave status check",
                "Human approval for critical roles"
            ]
        }
    }
    # ✅ Save daily snapshot for analytics
    save_daily_snapshot(request.json, staff_df)

    return jsonify(response), 200


# --------------------------------------------------
# 5. RUN APPLICATION
# --------------------------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
