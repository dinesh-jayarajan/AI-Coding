import calendar


def usingcalendar(datetuple):
    year, month, _ = datetuple

    if calendar.isleap(year):
        month = 2

    month_text = calendar.month(year, month)
    print(month_text)

    cal = calendar.Calendar(firstweekday=0)
    month_dates = list(cal.itermonthdates(year, month))

    last_week = month_dates[-7:]
    print(last_week)

    weekday_counts = [0] * 7
    first_seen_day = [None] * 7
    for d in month_dates:
        if d.month == month:
            w = d.weekday()
            weekday_counts[w] += 1
            if first_seen_day[w] is None:
                first_seen_day[w] = d.day

    max_count = max(weekday_counts)
    tied_weekdays = [w for w, c in enumerate(weekday_counts) if c == max_count]
    most_frequent_weekday = min(tied_weekdays, key=lambda w: first_seen_day[w])
    print(calendar.day_name[most_frequent_weekday])
