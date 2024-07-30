
def format_schedule_start_time(time_slot:str):
    """
    Formats the time slot to get only the start time.

    Example:
    >>> format_schedule_start_time("8:00 - 9:00")
    '800'

    >>> format_schedule_start_time("15:00 - 16:00")
    '1500'
    """
    return time_slot.split(":")[0] + time_slot.split(":")[1].split(" ")[0]
