# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Time related utilities and helper functions.
"""

import calendar
import datetime

import iso8601
import dateutil.tz as date_tz


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
PERFECT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def isotime(at=None):
    """Stringify time in ISO 8601 format"""
    if not at:
        at = utcnow()
    str = at.strftime(TIME_FORMAT)
    tz = at.tzinfo.tzname(None) if at.tzinfo else 'UTC'
    str += ('Z' if tz == 'UTC' else tz)
    return str


def utc_to_local(datetime_obj):
    '''
    parse a utc datetime to a local timezone datetime
    :param datetime_obj: a datetime object whose tzinfo is utc or None
    :retval : return a local timezone datetime object
    '''
    if not isinstance(datetime_obj, datetime.datetime):
        raise ValueError("'%s' is not a datetime object" % datetime_obj)
    if datetime_obj.tzinfo is None:
        datetime_obj = datetime_obj.replace(tzinfo=date_tz.tzutc())
    # no matter which timezone the datetime_obj is, change it as local
    datetime_obj = datetime_obj.astimezone(date_tz.tzlocal())
    return datetime_obj


def local_to_utc(datetime_obj):
    '''
    parse a local datetime to a local timezone datetime
    '''
    if not isinstance(datetime_obj, datetime.datetime):
        raise ValueError("'%s' is not a datetime object" % datetime_obj)
    if datetime_obj.tzinfo is None:
        datetime_obj = datetime_obj.replace(tzinfo=date_tz.tzlocal())
    # no matter which timezone the datetime_obj is, change it as local
    datetime_obj = datetime_obj.astimezone(date_tz.tzutc())
    return datetime_obj


def timestamp_to_datetime(timestamp):
    '''
    :param timestamp: millisecond timestamp
    :retval : return datetime object
    '''
    timestamp = int(timestamp) / 1000
    return datetime.datetime.fromtimestamp(timestamp)


def parse_isotime(timestr):
    """Parse time from ISO 8601 format"""
    try:
        return iso8601.parse_date(timestr)
    except iso8601.ParseError as e:
        raise ValueError(e.message)
    except TypeError as e:
        raise ValueError(e.message)


def strtime(at=None, fmt=PERFECT_TIME_FORMAT):
    """Returns formatted utcnow."""
    if not at:
        at = utcnow()
    return at.strftime(fmt)


def parse_strtime(timestr, fmt=PERFECT_TIME_FORMAT):
    """Turn a formatted time back into a datetime."""
    return datetime.datetime.strptime(timestr, fmt)


def normalize_time(timestamp):
    """Normalize time in arbitrary timezone to UTC"""
    offset = timestamp.utcoffset()
    return timestamp.replace(tzinfo=None) - \
                 offset if offset is not None else timestamp


def is_older_than(before, seconds):
    """Return True if before is older than seconds."""
    return utcnow() - before > datetime.timedelta(seconds=seconds)


def utcnow_ts():
    """Timestamp version of our utcnow function."""
    return calendar.timegm(utcnow().timetuple())


def utcnow():
    """Overridable version of utils.utcnow."""
    if utcnow.override_time:
        return utcnow.override_time
    return datetime.datetime.utcnow()


def seconds_ago(seconds):
    """return datetime object whose time is seconds from now."""
    return datetime.datetime.utcnow() - datetime.timedelta(seconds=seconds)


def seconds_from_now(before):
    """return total seconds from now"""
    return (datetime.datetime.utcnow() - before).total_seconds()

utcnow.override_time = None


def set_time_override(override_time=datetime.datetime.utcnow()):
    """Override utils.utcnow to return a constant time."""
    utcnow.override_time = override_time


def advance_time_delta(timedelta):
    """Advance overridden time using a datetime.timedelta."""
    assert(not utcnow.override_time is None)
    utcnow.override_time += timedelta


def advance_time_seconds(seconds):
    """Advance overridden time by seconds."""
    advance_time_delta(datetime.timedelta(0, seconds))


def clear_time_override():
    """Remove the overridden time."""
    utcnow.override_time = None


def marshall_now(now=None):
    """Make an rpc-safe datetime with microseconds.

    Note: tzinfo is stripped, but not required for relative times."""
    if not now:
        now = utcnow()
    return dict(day=now.day, month=now.month, year=now.year, hour=now.hour,
                minute=now.minute, second=now.second,
                microsecond=now.microsecond)


def unmarshall_time(tyme):
    """Unmarshall a datetime dict."""
    return datetime.datetime(day=tyme['day'], month=tyme['month'],
                 year=tyme['year'], hour=tyme['hour'], minute=tyme['minute'],
                 second=tyme['second'], microsecond=tyme['microsecond'])
