from automation_config import (
    EMERGENCY_PATIENT_THRESHOLD,
    AUTO_ALERT_ENABLED,
    AUTO_SHIFT_UPDATE_ENABLED,
    HUMAN_APPROVAL_REQUIRED_FOR
)

from alerts import bulk_alert
from shift_update import auto_update_shifts


class HospitalStaffingAgent:

    def __init__(self, model):
        self.model = model

    def assess_situation(self, predicted_patients):
        if predicted_patients >= EMERGENCY_PATIENT_THRESHOLD:
            return "EMERGENCY"
        return "NORMAL"

    def decide_actions(self, situation, staffing_plan):
        actions = []

        if situation == "EMERGENCY":
            actions.append("ACTIVATE_EMERGENCY_PROTOCOL")

        if staffing_plan:
            actions.append("DEPLOY_STAFF")

        return actions

    def execute(
        self,
        situation,
        staffing_plan,
        staff_df
    ):
        logs = []

        if situation == "EMERGENCY" and AUTO_ALERT_ENABLED:
            for dept, roles in staffing_plan.items():
                for role, staff_ids in roles.items():

                    if role in HUMAN_APPROVAL_REQUIRED_FOR:
                        logs.append(
                            f"Human approval required for role: {role}"
                        )
                        continue

                    message = f"Emergency duty assigned in {dept}"
                    bulk_alert(staff_ids, message)
                    logs.append(
                        f"Auto-alert sent to {len(staff_ids)} {role}s"
                    )

        if AUTO_SHIFT_UPDATE_ENABLED:
            all_staff = []
            for dept in staffing_plan:
                for role in staffing_plan[dept]:
                    all_staff.extend(staffing_plan[dept][role])

            staff_df = auto_update_shifts(staff_df, all_staff)
            logs.append("Shift schedule auto-updated")

        return staff_df, logs
