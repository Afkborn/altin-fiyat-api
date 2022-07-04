from datetime import datetime as dt


def get_time():
    return dt.now().strftime("%H:%M %d.%m.%Y")

def get_time_command():
    return dt.now().strftime("%H:%M:%S.%f")

def get_time_from_unix(unix_time : str):
    return dt.fromtimestamp(unix_time).strftime("%Y-%m-%d")


def get_last_date():
    return dt.now().strftime("%Y-%m-%d")
