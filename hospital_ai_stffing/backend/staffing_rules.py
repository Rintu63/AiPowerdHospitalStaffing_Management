def staff_requirements(predicted):
    """
    Urban hospital staffing rules
    """
    return {
        "ICU": {
            "Doctor": max(1, predicted // 25),
            "Nurse": max(2, predicted // 8),
            "Sister": max(1, predicted // 15)
        },
        "Emergency": {
            "Doctor": max(1, predicted // 30),
            "Nurse": max(2, predicted // 10)
        },
        "Ward": {
            "Nurse": max(2, predicted // 20),
            "Cleaner": max(1, predicted // 40)
        },
        "Pharmacy": {
            "Pharmacist": max(1, predicted // 50)
        },
        "Security": {
            "Security": max(2, predicted // 60)
        },
        "Housekeeping": {
            "Cleaner": max(2, predicted // 50)
        }
    }
