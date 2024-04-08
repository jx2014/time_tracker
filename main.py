import datetime
from datetime import datetime as dt

time_format = "%m/%d/%Y %H:%M"

start_date = "1/1/2024 15:30"
start_offset = 24  # in hours
dt_start_offset = datetime.timedelta(hours=start_offset)
dt_start_date = dt.strptime(start_date, time_format) + dt_start_offset
check_intervals = [250, 500, 750, 1000, 1250, 1500, 1750]
test_stops = []
test_stops = [{"stop": "1/5/2024 12:00", "resume": "1/10/2024 12:00"},
              {"stop": "1/15/2024 12:00", "resume": "1/20/2024 12:00"},
              {"stop": "2/15/2024 12:00", "resume": "3/10/2024 12:00"},
              ]


def get_net_hours(time_delta) -> int:
    return time_delta.seconds / 3600 + time_delta.days * 24


def get_new_date_from_hours(input_time, time_hours: int) -> datetime.datetime:
    return input_time + datetime.timedelta(hours=time_hours)


def show_time(input_time, t: int, comments=""):
    time_string = input_time.strftime(time_format)
    print("    T=%-4d %s %s" % (t, time_string, comments))


start_t = dt_start_date
net_hour = 0
show_time(start_t, net_hour)
for stop in test_stops:
    stop_t = dt.strptime(stop.get("stop"), time_format)
    resumed_net_hour = net_hour
    net_hour = get_net_hours(stop_t - start_t) + net_hour
    remove_idx = 0
    for i in range(len(check_intervals)):
        check_interval = check_intervals[i]
        if check_interval > net_hour:
            show_time(stop_t, net_hour, "stopped")
            break

        display_time = get_new_date_from_hours(start_t, check_interval - resumed_net_hour)
        show_time(display_time, check_interval)
        remove_idx += 1

    check_intervals = check_intervals[remove_idx:]
    try:
        start_t = dt.strptime(stop.get("resume"), time_format)
        show_time(start_t, net_hour, comments="resumed")
    except TypeError:
        start_t = None
        break

if not start_t:
    exit()

# show remaining check points if test has been resumed:
for i in range(len(check_intervals)):
    check_interval = check_intervals[i]
    display_time = get_new_date_from_hours(start_t, check_interval - net_hour)
    show_time(display_time, check_interval)
