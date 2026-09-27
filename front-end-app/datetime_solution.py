import datetime


def dateandtime(val, tup):
    result = []

    if val == 1:
        d = datetime.date(tup[0], tup[1], tup[2])
        result.append(d)
        result.append(d.strftime("%d/%m/%Y"))

    elif val == 2:
        # Use UTC conversion to keep output deterministic across environments.
        d = datetime.datetime.utcfromtimestamp(tup[0]).date()
        result.append(d)

    elif val == 3:
        t = datetime.time(tup[0], tup[1], tup[2])
        result.append(t)
        result.append(t.strftime("%I"))

    elif val == 4:
        d = datetime.date(tup[0], tup[1], tup[2])
        result.append(d.strftime("%A"))
        result.append(d.strftime("%B"))
        result.append(d.strftime("%j"))

    elif val == 5:
        dt = datetime.datetime(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        result.append(dt)

    return result
