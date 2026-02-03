# backend/emergency.py

def select_staff(
    on_duty_df,
    off_duty_df,
    role,
    department,
    count
):
    """
    Select staff for a given role & department.
    Priority:
    1. On-duty staff
    2. Off-duty but emergency-eligible staff
    """

    selected = []

    # 1️⃣ On-duty staff first
    eligible_on_duty = on_duty_df[
        (on_duty_df["role"] == role) &
        (on_duty_df["department"] == department)
    ]

    for _, row in eligible_on_duty.iterrows():
        if len(selected) < count:
            selected.append(row["staff_id"])

    # 2️⃣ Off-duty emergency staff
    if len(selected) < count:
        eligible_off_duty = off_duty_df[
            (off_duty_df["role"] == role) &
            (off_duty_df["department"] == department)
        ]

        for _, row in eligible_off_duty.iterrows():
            if len(selected) < count:
                selected.append(row["staff_id"])

    return selected
