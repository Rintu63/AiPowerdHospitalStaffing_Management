import time

def event_loop(agent, predict_func, get_staffing_plan, staff_df):
    """
    Continuous AI automation loop
    """
    while True:
        predicted_patients = predict_func()
        situation = agent.assess_situation(predicted_patients)

        if situation == "EMERGENCY":
            staffing_plan = get_staffing_plan(predicted_patients)
            staff_df, logs = agent.execute(
                situation,
                staffing_plan,
                staff_df
            )

            print("🤖 AI Automation Logs:")
            for log in logs:
                print(" -", log)

        time.sleep(60)  # check every minute
