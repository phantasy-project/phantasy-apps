# -*- coding: utf-8 -*-


def uptime(t):
    """Convert *t* in second to uptime with the tuple of days, hours,
    minutes, and seconds, and return string of uptime.

    Examples
    --------
    >>> assert uptime(12345) == "03:25:45"
    >>> assert uptime(123455) == "1 day, 10:17:35"
    >>> assert uptime(1234555) == "14 days, 06:55:55"
    """
    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24

    days = int(t / DAY)
    hours = int((t % DAY) / HOUR)
    minutes = int((t % HOUR) / MINUTE)
    seconds = int(t % MINUTE)

    s = ''
    if days > 0:
        s += str(days) + " " + (days == 1 and "day" or "days") + ", "
    s += '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    return s


if __name__ == '__main__':
    t = 12345
    assert uptime(t) == "03:25:45"

    t = 123455
    assert uptime(t) == "1 day, 10:17:35"

    t = 1234555
    assert uptime(t) == "14 days, 06:55:55"
