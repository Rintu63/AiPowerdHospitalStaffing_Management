import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

AUDIT_LOG_PATH = os.path.join("data", "audit_log.csv")

def log_event(event_type, description):
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_type,
        "description": description
    }

    if os.path.exists(AUDIT_LOG_PATH):
        df = pd.read_csv(AUDIT_LOG_PATH)
        df = pd.concat([df, pd.DataFrame([log])], ignore_index=True)
    else:
        df = pd.DataFrame([log])

    df.to_csv(AUDIT_LOG_PATH, index=False)

# STAFF ID GENERATOR (ADD HERE )
def generate_staff_id(role, staff_df):
    """
    Auto-generate unique staff ID based on role & year
    """
    year = datetime.now().year

    role_prefix = {
        "Doctor": "DOC",
        "Nurse": "NUR",
        "Sister": "SIS",
        "Pharmacist": "PHA",
        "Cleaner": "CLN",
        "Security": "SEC"
    }.get(role, "STF")

    # If staff_df has no staff_id column or is empty, start numbering at 1
    if not isinstance(staff_df, pd.DataFrame) or staff_df.empty or "staff_id" not in staff_df.columns:
        next_number = 1
    else:
        role_ids = staff_df.loc[
            staff_df["staff_id"].astype(str).str.startswith(role_prefix, na=False),
            "staff_id"
        ]

        if role_ids.empty:
            next_number = 1
        else:
            last_number = (
                role_ids
                .str.split("-")
                .str[-1]
                .astype(int)
                .max()
            )
            next_number = last_number + 1

    return f"{role_prefix}-{year}-{str(next_number).zfill(4)}"


# =====================================================
# CONFIG
# =====================================================
BACKEND_URL = "http://127.0.0.1:5000"
DATA_PATH = os.path.join("data", "staff_schedule.csv")

SNAPSHOT_PATH = os.path.join("data", "daily_snapshot.csv")

def load_snapshots():
    if not os.path.exists(SNAPSHOT_PATH):
        return pd.DataFrame()
    df = pd.read_csv(SNAPSHOT_PATH, parse_dates=["date"])
    return df


st.set_page_config(
    page_title="Urban Hospital AI Control Panel",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# STYLE (MODERN, CREATIVE DESIGN)
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Poppins:wght@600;700;800&display=swap');

/* ===== App Background ===== */
.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
    color: #E2E8F0;
}

/* ===== Main Container ===== */
.block-container {
    padding: 2rem 2.5rem;
    max-width: 1600px;
}

/* ===== Global Font ===== */
* {
    font-family: 'Inter', sans-serif;
}

/* ===== Headings - Modern & Bold ===== */
h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(120deg, #60A5FA, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}

h2 {
    font-family: 'Poppins', sans-serif;
    color: #E0F2FE;
    font-weight: 700;
    font-size: 1.75rem;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #60A5FA;
    padding-left: 1rem;
}

h3, h4 {
    color: #CBD5E1;
    font-weight: 600;
    font-size: 1.2rem;
}

/* ===== Caption & Subtext ===== */
.stMarkdown > p {
    color: #94A3B8;
    font-size: 1rem;
    line-height: 1.6;
}

/* ===== Cards & Containers ===== */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #475569;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #60A5FA;
    box-shadow: 0 12px 32px rgba(96, 165, 250, 0.2);
}

/* ===== Metric Value Color ===== */
div[data-testid="stMetricValue"] {
    color: #60A5FA;
    font-weight: 700;
    font-size: 2rem;
}

div[data-testid="stMetricLabel"] {
    color: #CBD5E1;
    font-weight: 500;
}

/* ===== Buttons - Modern Style ===== */
.stButton > button {
    background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
    color: white;
    border-radius: 12px;
    padding: 0.7rem 1.5rem;
    font-weight: 600;
    border: none;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
    transform: translateY(-2px);
}

.stButton > button:active {
    transform: translateY(0);
}

/* ===== Input Fields ===== */
input, textarea, select {
    background-color: #1E293B !important;
    border: 1.5px solid #475569 !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    padding: 0.75rem !important;
    font-weight: 500;
    transition: all 0.2s ease;
}

input:focus, textarea:focus, select:focus {
    border-color: #60A5FA !important;
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1) !important;
    background-color: #0F172A !important;
}

/* ===== Tabs ===== */
div[data-baseweb="tab-list"] {
    border-bottom: 2px solid #334155;
}

div[data-baseweb="tab-list"] button {
    background-color: transparent;
    color: #94A3B8;
    font-weight: 600;
    font-size: 1rem;
    padding: 1rem 1.5rem;
    transition: all 0.3s ease;
    border-bottom: 2px solid transparent;
}

div[data-baseweb="tab-list"] button:hover {
    color: #CBD5E1;
}

div[data-baseweb="tab-list"] button[aria-selected="true"] {
    border-bottom: 3px solid #60A5FA;
    color: #60A5FA;
}

/* ===== Alert Boxes ===== */
.stAlert {
    border-radius: 12px;
    border-left: 4px solid;
    padding: 1rem;
    background-color: rgba(30, 41, 59, 0.8);
}

.stAlert[data-testid="info-alert"] {
    border-left-color: #3B82F6;
    background-color: rgba(59, 130, 246, 0.1);
}

.stAlert[data-testid="success-alert"] {
    border-left-color: #10B981;
    background-color: rgba(16, 185, 129, 0.1);
}

.stAlert[data-testid="warning-alert"] {
    border-left-color: #F59E0B;
    background-color: rgba(245, 158, 11, 0.1);
}

.stAlert[data-testid="error-alert"] {
    border-left-color: #EF4444;
    background-color: rgba(239, 68, 68, 0.1);
}

/* ===== Risk Level Colors ===== */
.risk-low {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
    color: #A7F3D0;
    padding: 1rem;
    border-radius: 12px;
    border-left: 4px solid #10B981;
    font-weight: 600;
}

.risk-medium {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.05));
    color: #FCD34D;
    padding: 1rem;
    border-radius: 12px;
    border-left: 4px solid #F59E0B;
    font-weight: 600;
}

.risk-high {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.05));
    color: #FCA5A5;
    padding: 1rem;
    border-radius: 12px;
    border-left: 4px solid #EF4444;
    font-weight: 600;
}

/* ===== Expander ===== */
div[data-testid="stExpander"] {
    border: 1px solid #475569;
    border-radius: 12px;
    background-color: rgba(30, 41, 59, 0.5);
}

/* ===== Code Block ===== */
code {
    background-color: #0F172A;
    color: #60A5FA;
    border-radius: 8px;
    padding: 0.25rem 0.5rem;
    font-weight: 500;
}

/* ===== Dataframe ===== */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* ===== Progress Bar ===== */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #3B82F6 0%, #60A5FA 100%);
    border-radius: 10px;
}

/* ===== Divider ===== */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #475569, transparent);
    margin: 2rem 0;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD STAFF DATA
# =====================================================
def load_staff():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)

def save_staff(df):
    df.to_csv(DATA_PATH, index=False)

staff_df = load_staff()

# =====================================================
# HEADER
# =====================================================
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.title("🏥 Hospital Command Dashboard")
    st.caption("⚡ AI-Powered Staffing • Real-time Operations • Intelligent Scheduling")

with header_col2:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div style="text-align: right; padding: 1rem; background: linear-gradient(135deg, #1E293B, #334155); 
    border-radius: 12px; border: 1px solid #475569;">
    <div style="color: #94A3B8; font-size: 0.9rem;">System Time</div>
    <div style="color: #60A5FA; font-size: 1.8rem; font-weight: bold; font-family: 'Courier New';">{current_time}</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3, tab4, tab5= st.tabs([
    "AI Staffing Overview",
    "Staff Directory",
    "Edit Staff",
    "Add New Staff",
    "Analytics & Trends"
])

# =====================================================
# TAB 1 – AI STAFFING OVERVIEW
# =====================================================
with tab1:
    st.markdown("<h2 style='margin-top: 0;'>🤖 AI Staffing Decision Engine</h2>", unsafe_allow_html=True)

    st.markdown("### Current Patient Census")
    col1, col2, col3 = st.columns(3)
    opd = col1.number_input("🏥 OPD Patients", 0, 3000, 300)
    emergency = col2.number_input("🚑 Emergency Patients", 0, 1500, 120)
    icu = col3.number_input("🔴 ICU Patients", 0, 800, 45)

    st.markdown("---")
    st.markdown("### Department Capacity Status")

    col_o1, col_o2 = st.columns(2)

    icu_occupancy = col_o1.slider(
        "🏥 ICU Occupancy Level", 0, 100, 70, help="Current ICU bed utilization"
    )

    er_occupancy = col_o2.slider(
        "🚑 Emergency Occupancy Level", 0, 100, 65, help="Current Emergency room capacity"
    )

    st.markdown("---")
    st.markdown("### Available Staff Resources")
    col4, col5 = st.columns(2)
    nurses = col4.number_input("👩‍⚕️ Available Nurses", 0, 800, 90)
    doctors = col5.number_input("👨‍⚕️ Available Doctors", 0, 500, 40)

    st.markdown("---")
    st.markdown("### 🔴 Patient Severity Distribution")

    col_s1, col_s2, col_s3 = st.columns(3)

    critical_pct = col_s1.slider(
        "🔴 Critical Patients (%)", 0, 100, 20, help="Percentage requiring immediate intensive care"
    )

    moderate_pct = col_s2.slider(
        "🟠 Moderate Patients (%)", 0, 100, 50, help="Percentage requiring standard ward care"
    )

    stable_pct = col_s3.slider(
        "🟢 Stable Patients (%)", 0, 100, 30, help="Percentage in recovery or observation"
    )

    st.markdown("---")
    st.markdown("###  Staff Workload Indicators")

    col_f1, col_f2 = st.columns(2)
    fatigued_staff_pct = col_f1.slider(
        "Staff on Extended Shifts (%)", 0, 100, 25, help="Percentage of staff working overtime"
    )
    transport_issue = col_f2.selectbox(
        "🚗 Staff Transport Disruption", ["✅ No", "⚠️ Yes"], help="Any known transportation issues"
    )
    
    st.markdown("---")
    st.markdown("###  Operational Context")

    col_t1, col_t2 = st.columns(2)
    shift_type = col_t1.selectbox(
        " Current Shift", [" Morning", "Evening", " Night"], help="Select active shift period"
    )
    special_day = col_t2.selectbox(
        "📅 Special Day", ["Normal Day", " Festival", " Public Holiday"], help="Any special circumstances"
    )
    
    st.markdown("---")
    st.markdown("### External Risk Factors")
    external_risk = st.selectbox(
        "External Risk Level",
        ["✅ None", "🌧️ Weather Alert", "🚨 Accident Nearby", "🦠 Disease Outbreak"],
        help="Any external factors affecting operations"
    )
    payload = {
        "opd_patients": opd,
        "emergency_patients": emergency,
        "icu_patients": icu,
        "available_nurses": nurses,
        "available_doctors": doctors,

        "severity_mix": {
            "critical": critical_pct,
            "moderate": moderate_pct,
            "stable": stable_pct
        },
        "occupancy": {
            "icu": icu_occupancy,
            "er": er_occupancy
        },
        "staff_pressure": {
            "fatigued_pct": fatigued_staff_pct,
            "transport_issue": "yes" if transport_issue.startswith("✅") else "yes" if transport_issue.startswith("⚠️") else "no"
        },
        "time_context": {
            "shift": shift_type.split()[-1].lower(),
            "special_day": special_day.split()[-1].lower() if special_day != "Normal Day" else "normal"
        },
        "external_risk": external_risk.split()[-1].lower() if not external_risk.startswith("✅") else "none"
    }

    st.markdown("---")
    
    if st.button("🚀 Run AI Staffing Decision", use_container_width=True):
        if opd + emergency + icu == 0:
            st.warning("Patient count is zero. AI decision may not be meaningful.")
        try:
            res = requests.post(f"{BACKEND_URL}/urban_ai_staffing", json=payload)
            data = res.json()
            # =============================
            # 🚦 RISK SCORE VISUALIZATION
            # =============================
            st.markdown("---")
            st.markdown("## 🚦 Operational Risk Assessment")

            risk_score = data["risk_assessment"]["risk_score"]
            risk_level = data["risk_assessment"]["risk_level"]

            # Color logic
            if risk_level == "LOW":
                bar_color = "#10B981"
                risk_emoji = "✅"
            elif risk_level == "MEDIUM":
                bar_color = "#F59E0B"
                risk_emoji = "⚠️"
            else:
                bar_color = "#EF4444"
                risk_emoji = "🔴"

            col_risk1, col_risk2 = st.columns([2, 1])
            
            with col_risk1:
                st.progress(risk_score / 100)
            
            with col_risk2:
                st.markdown(
                    f"""
                    <div style="
                        padding: 1rem;
                        border-radius: 12px;
                        background: linear-gradient(135deg, {bar_color}20, {bar_color}10);
                        border: 2px solid {bar_color};
                        text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{risk_emoji}</div>
                        <div style="color: {bar_color}; font-weight: bold; font-size: 1.2rem;">
                            {risk_level}
                        </div>
                        <div style="color: {bar_color}; font-size: 1.8rem; font-weight: 800;">
                            {risk_score}/100
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.markdown("---")
            # =============================
            # 🧠 AI DECISION EXPLANATION
            # =============================
            st.markdown("## 🧠 AI Intelligence Report")

            decision_mode = data["patient_prediction"]["decision_mode"]

            explanation_points = []

            if risk_level == "HIGH":
                explanation_points.append("🔴 High operational risk detected due to severity, occupancy, or external factors.")
            if icu_occupancy > 75:
                explanation_points.append("ICU occupancy is critically high—immediate resource allocation needed.")
            if critical_pct > 30:
                explanation_points.append("⚠️ High percentage of critical patients requiring intensive intervention.")
            if fatigued_staff_pct > 30:
                explanation_points.append(" Significant staff fatigue detected—consider bringing additional staff.")
            if not external_risk.startswith("✅"):
                risk_name = external_risk.split()[-1] if len(external_risk.split()) > 1 else external_risk
                explanation_points.append(f" External risk present: {risk_name}—increased vigilance required.")
            if "Night" in shift_type:
                explanation_points.append(" Night shift operations—typically require more careful monitoring.")

            col_mode1, col_mode2, col_mode3 = st.columns(3)
            
            with col_mode1:
                col_mode1.metric("Decision Mode", decision_mode)
            with col_mode2:
                col_mode2.metric(" Predicted Patients", data["patient_prediction"]["predicted_total_patients"])
            with col_mode3:
                col_mode3.metric(" Blocked Staff", data["staff_status_summary"]["blocked_staff_count"])

            if explanation_points:
                st.markdown("### 📌 Key Insights")
                for point in explanation_points:
                    st.markdown(f"- {point}")
            else:
                st.success("✅ All systems nominal—operations running smoothly!")

            log_event(
                "AI_DECISION",
                f"Predicted={data['patient_prediction']['predicted_total_patients']}, "
                f"Mode={data['patient_prediction']['decision_mode']}"
            )

            st.markdown("---")
            st.markdown("## 👥 Department Staffing Deployment Plan")

            for dept, roles in data["staffing_plan"].items():
                with st.expander(f"🏥 {dept} Department", expanded=(dept == "ICU")):
                    dept_cols = st.columns(len(roles))
                    
                    for idx, (role, ids) in enumerate(roles.items()):
                        with dept_cols[idx]:
                            st.markdown(f"**{role}**")
                            st.info(f"**{len(ids)}** staff assigned")
                            if ids:
                                st.code(", ".join(ids), language="")
                            else:
                                st.warning("❌ No eligible staff available")

        except Exception as e:
            st.error("❌ Backend not reachable or error occurred")

# =====================================================
# TAB 2 – STAFF MANAGEMENT (VIEW / DELETE)
# =====================================================
with tab2:
    st.subheader("Staff Directory")

    if staff_df.empty:
        st.warning("No staff data available")
    else:
        search = st.text_input("Search by Name / Role / Department")

        filtered_df = staff_df
        if search:
            filtered_df = staff_df[
                staff_df.apply(
                    lambda row: search.lower() in row.astype(str).str.lower().to_string(),
                    axis=1
                )
            ]

        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("###  Remove Staff")

        staff_id_to_delete = st.selectbox(
            "Select Staff ID to Delete",
            options=[""] + staff_df["staff_id"].tolist()
        )

        if st.button("Delete Selected Staff"):
            if staff_id_to_delete:
                staff_df = staff_df[staff_df["staff_id"] != staff_id_to_delete]
                save_staff(staff_df)
                st.success(f"Staff {staff_id_to_delete} removed")
                st.rerun()
                
                st.markdown("###  Audit Log")
                if os.path.exists(AUDIT_LOG_PATH):
                    audit_df = pd.read_csv(AUDIT_LOG_PATH)
                    st.dataframe(audit_df.tail(50), use_container_width=True)
                else:
                    st.info("No audit logs yet")


# =====================================================
# TAB 3 – ADD NEW STAFF
# =====================================================
with tab3:
    st.subheader("Add New Staff")

    staff_df = load_staff()

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Staff Name")
        role = st.selectbox(
            "Role",
            ["Doctor", "Nurse", "Sister", "Pharmacist", "Cleaner", "Security"]
        )

    with col2:
        department = st.selectbox(
            "Department",
            ["OPD", "Emergency", "ICU", "Ward", "Pharmacy", "Administration"]
        )
        shift = st.selectbox(
            "Shift",
            ["Morning", "Evening", "Night"]
        )

    # 🔥 AUTO-GENERATE STAFF ID
    if role:
        staff_id = generate_staff_id(role, staff_df)
        st.info(f"🆔 Auto-Generated Staff ID: **{staff_id}**")

    if st.button("✅ Add Staff"):
        if not name.strip():
            st.warning("Staff name is required.")
        else:
            new_staff = {
                "staff_id": staff_id,
                "name": name,
                "role": role,
                "department": department,
                "shift": shift,
                "status": "Active"
            }

            staff_df = pd.concat(
                [staff_df, pd.DataFrame([new_staff])],
                ignore_index=True
            )

            staff_df.to_csv(DATA_PATH, index=False)

            st.success(f"Staff {name} added successfully!")
            st.rerun()


# =====================================================
# TAB 4 – EDIT STAFF (REALISTIC & IMPORTANT)
# =====================================================
with tab4:
    st.subheader("Update Staff Status")

    if staff_df.empty:
        st.warning("No staff data available")
    else:
        staff_id = st.selectbox(
            "Select Staff ID",
            staff_df["staff_id"].tolist()
        )

        staff_row = staff_df[staff_df["staff_id"] == staff_id].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            on_duty = st.selectbox(
                "On Duty",
                ["yes", "no"],
                index=0 if staff_row["on_duty"] == "yes" else 1
            )

            on_leave = st.selectbox(
                "On Leave",
                ["no", "yes"],
                index=0 if staff_row["on_leave"] == "no" else 1
            )

            burnout_options = ["LOW", "MODERATE", "HIGH"]
            burnout_value = staff_row.get("burnout_risk", "LOW")
            burnout_index = burnout_options.index(burnout_value) if burnout_value in burnout_options else 0
            
            burnout = st.selectbox(
                "Burnout Risk",
                burnout_options,
                index=burnout_index
            )

        with col2:
            dept_options = sorted(staff_df["department"].unique().tolist())
            dept_value = staff_row.get("department", dept_options[0] if dept_options else "OPD")
            dept_index = dept_options.index(dept_value) if dept_value in dept_options else 0
            
            department = st.selectbox(
                "Department",
                dept_options,
                index=dept_index
            )

            emergency_eligible = st.selectbox(
                "Emergency Eligible",
                ["yes", "no"],
                index=0 if staff_row["emergency_eligible"] == "yes" else 1
            )

        if st.button(" Save Changes"):
            staff_df.loc[
                staff_df["staff_id"] == staff_id,
                ["on_duty", "on_leave", "burnout_risk", "department", "emergency_eligible"]
            ] = [
                on_duty, on_leave, burnout, department, emergency_eligible
            ]

            save_staff(staff_df)

            st.success(f"Staff {staff_id} updated successfully")
            st.rerun()
            
with tab5:
    st.subheader(" Staffing & Patient Trends")

    df = load_snapshots()

    if df.empty:
        st.warning("No historical data available yet.")
    else:
        # -----------------------------
        # TIME RANGE SELECTOR
        # -----------------------------
        period = st.selectbox(
            "Select Time Range",
            ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"]
        )

        df_sorted = df.sort_values("date")

        if period == "Weekly":
            df_plot = df_sorted.resample("W", on="date").mean()
        elif period == "Monthly":
            df_plot = df_sorted.resample("M", on="date").mean()
        elif period == "Quarterly":
            df_plot = df_sorted.resample("Q", on="date").mean()
        elif period == "Yearly":
            df_plot = df_sorted.resample("Y", on="date").mean()
        else:
            df_plot = df_sorted.set_index("date")

        st.markdown("###  Staff Availability Over Time")
        st.line_chart(
            df_plot[["doctors", "nurses", "sisters"]]
        )

        st.markdown("###  Patient Load Over Time")
        st.line_chart(
            df_plot[
                ["patients_opd", "patients_emergency", "patients_icu"]
            ]
        )
