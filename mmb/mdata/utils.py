from django.utils import timezone


def get_time_diff(time1, time2=timezone.now()):
    """
    gives the time difference in minutes and seconds
    :param time1: given time
    :param time2: default as current time
    :return: tuple of minutes and seconds
    """
    time_delta = time1 - time2
    return divmod(time_delta.days * 86400 + time_delta.seconds, 60)



