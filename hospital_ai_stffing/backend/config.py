"""
Central configuration file
All paths and constants are defined here
"""

import os

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths
MODEL_PATH = os.path.join(BASE_DIR, "models", "demand_model.pkl")
STAFF_DATA_PATH = os.path.join(BASE_DIR, "data", "staff_schedule.csv")

# Safety & system constants (can be expanded later)
MAX_SHIFT_HOURS = 10
MAX_CONSECUTIVE_DAYS = 6

# Automation threshold
EMERGENCY_PATIENT_THRESHOLD = 700
