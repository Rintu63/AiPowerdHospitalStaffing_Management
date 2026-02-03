import pandas as pd

def load_staff(path):
    return pd.read_csv(path)

def classify_staff(df):
    on_duty = df[
        (df["on_duty"] == "yes") &
        (df["on_leave"] == "no")
    ]

    off_duty_ready = df[
        (df["on_duty"] == "no") &
        (df["on_leave"] == "no") &
        (df["burnout_risk"] != "HIGH") &
        (df["emergency_eligible"] == "yes")
    ]

    blocked = df[
        (df["on_leave"] == "yes") |
        (df["burnout_risk"] == "HIGH")
    ]

    return on_duty, off_duty_ready, blocked
