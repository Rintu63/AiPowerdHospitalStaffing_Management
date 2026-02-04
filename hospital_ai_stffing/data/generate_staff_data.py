import pandas as pd
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

STAFF_COUNT = 250

roles = [
    "Doctor", "Nurse", "Sister", "Pharmacist",
    "Lab_Technician", "Radiologist",
    "Cleaner", "Security", "Admin_Staff"
]

departments = [
    "ICU", "Emergency", "OPD", "Surgery",
    "Radiology", "Pharmacy", "Laboratory",
    "Ward", "Administration", "Security", "Housekeeping"
]

burnout_levels = ["LOW", "MODERATE", "HIGH"]

rows = []

for i in range(1, STAFF_COUNT + 1):
    role = random.choice(roles)

    # Logical department assignment
    if role == "Doctor":
        dept = random.choice(["ICU", "Emergency", "OPD", "Surgery"])
    elif role in ["Nurse", "Sister"]:
        dept = random.choice(["ICU", "Emergency", "Ward"])
    elif role == "Pharmacist":
        dept = "Pharmacy"
    elif role == "Lab_Technician":
        dept = "Laboratory"
    elif role == "Radiologist":
        dept = "Radiology"
    elif role == "Cleaner":
        dept = "Housekeeping"
    elif role == "Security":
        dept = "Security"
    else:
        dept = "Administration"

    rows.append({
        "staff_id": f"S{i:03d}",
        "name": f"Staff_{i}",
        "role": role,
        "department": dept,
        "on_duty": random.choice(["yes", "no"]),
        "on_leave": random.choice(["no", "no", "no", "yes"]),
        "last_shift_hours": random.randint(0, 12),
        "burnout_risk": random.choice(burnout_levels),
        "emergency_eligible": "yes" if role not in ["Cleaner", "Admin_Staff"] else "no"
    })

df = pd.DataFrame(rows)
df.to_csv(os.path.join(DATA_DIR, "staff_schedule.csv"), index=False)

print("✅ 250+ urban hospital staff generated")
print(df.head())
