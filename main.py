import datetime
from datetime import datetime as dt

time_format = "%m/%d/%Y %H:%M"

start_date = "1/1/2024 15:30"
start_offset = 24  # in hours
dt_start_offset = datetime.timedelta(hours=start_offset)
dt_start_date = dt.strptime(start_date, time_format) + dt_start_offset
check_intervals = [250, 500, 750, 1000, 1250, 1500, 1750]
all_events = [{"type": "event", "date": "1/4/2024 12:00", "comment": "event 1"},
              {"type": "event", "date": "3/6/2024 12:00", "comment": "event 2"}, ]

all_events = []

all_events = [{"type": "event", "date": "1/4/2024 12:00", "comment": "event 1"},
              {"type": "stop", "date": "1/5/2024 12:00", "comment": "stop reason 1"},
              {"type": "resume", "date": "1/10/2024 12:00", "comment": "resume from 1"},  # T=68
              {"type": "event", "date": "1/13/2024 12:00", "comment": "event 2"},
              {"type": "event", "date": "1/14/2024 12:00", "comment": "event 3"},
              {"type": "stop", "date": "1/15/2024 12:00", "comment": "stop reason 2"},  # T=188
              {"type": "resume", "date": "1/20/2024 12:00", "comment": "resume from 2"},
              {"type": "stop", "date": "2/15/2024 12:00", "comment": "stop reason 3"},  # T=812
              {"type": "resume", "date": "3/10/2024 12:00", "comment": "resume from 3"}
              ]




def get_net_hours(time_delta) -> int:
    return time_delta.seconds / 3600 + time_delta.days * 24


def get_new_date_from_hours(input_time, time_hours: int) -> datetime.datetime:
    return input_time + datetime.timedelta(hours=time_hours)


def show_time(input_time, t: int, comments=""):
    time_string = input_time.strftime(time_format)
    print("    T=%-4d %s %s" % (t, time_string, comments))


start_t = dt_start_date
net_hour_since_last_resume = 0
total_net_hour = 0
show_time(start_t, net_hour_since_last_resume)
for event in all_events:
    event_type = event.get("type")
    event_datetime = event.get("date")
    event_comment = event.get("comment", "")
    event_t = dt.strptime(event_datetime, time_format)
    net_hour_since_last_resume = get_net_hours(event_t - start_t)

    if event_type == "event":
        remove_idx = 0
        for i in range(len(check_intervals)):
            check_interval = check_intervals[i]
            event_hours = net_hour_since_last_resume + total_net_hour
            if check_interval > event_hours:
                show_time(event_t, event_hours, event_comment)
                break
            display_t = get_new_date_from_hours(start_t, check_interval - total_net_hour)
            show_time(display_t, check_interval)
            remove_idx += 1
        check_intervals = check_intervals[remove_idx:]
        continue

    if event_type == "stop":
        total_net_hour = net_hour_since_last_resume + total_net_hour
        remove_idx = 0
        for i in range(len(check_intervals)):
            check_interval = check_intervals[i]
            if check_interval > total_net_hour:
                show_time(event_t, total_net_hour, event_comment)
                break
            display_t = get_new_date_from_hours(start_t,
                                                check_interval - (total_net_hour - net_hour_since_last_resume))
            show_time(display_t, check_interval)
            remove_idx += 1
        check_intervals = check_intervals[remove_idx:]
        continue

    if event_type == "resume":
        start_t = event_t
        show_time(start_t, total_net_hour, comments=event_comment)

if not start_t:
    exit()

# show remaining check points if test has been resumed:
for i in range(len(check_intervals)):
    check_interval = check_intervals[i]
    display_t = get_new_date_from_hours(start_t, check_interval - total_net_hour)
    show_time(display_t, check_interval)
