def auto_update_shifts(staff_df, activated_staff_ids):
    """
    Automatically mark selected staff as on-duty
    """
    staff_df.loc[
        staff_df["staff_id"].isin(activated_staff_ids),
        "on_duty"
    ] = "yes"

    return staff_df
