import re
import datetime as dt


file_name = "ReportExport.rtf"

def get_lines_from_file(f):
    matches = []
    regex_string = r"\s(\d{2}.\d{2})((?:\s{1,2}\d{4})+)"
    for line in f:
        match = re.search(regex_string, line)
        if match != None:
            matches.append(match.groups())
    return matches


def match_to_times(match):
    year = dt.datetime.now().year
    day, month = match[0].split(".")
    times = match[1].split()
    datetimes = [dt.datetime(year, int(month), int(day), int(
        time[:2]), int(time[2:])) for time in times]
    return datetimes


def calculate_leaving_time(datetimes, target_time="8:30"):
    h, m = target_time.split(":")
    target_time = dt.timedelta(hours=int(h), minutes=int(m))
    worked = dt.timedelta(0)
    now = dt.datetime.now().replace(second=0, microsecond=0)
    i = 1
    while i < len(datetimes):
        worked += datetimes[i] - datetimes[i-1]
        i += 2
    if len(datetimes) % 2 == 0:
        print(
            f"You have worked {worked} so far and are currently off the clock.")
    else:
        worked += now - datetimes[-1]
        print(
            f"You have worked {worked} so far and are currently on the clock.")
    if worked < target_time:
        print(
            f"You will be finished at {now+target_time-worked}.")
    else:
        print(f"You made {worked-target_time} of overtime so far.")

def main(file_name="ReportExport.rtf", target_time="8:30"):
    with open(file_name, "r") as f:
        matches = get_lines_from_file(f)
        calculate_leaving_time(match_to_times(matches[-1]), target_time)

if __name__ == "__main__":
    main()
