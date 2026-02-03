import datetime

def send_alert(staff_id, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 📲 Alert sent to {staff_id}: {message}")

def bulk_alert(staff_list, message):
    for staff in staff_list:
        send_alert(staff, message)
