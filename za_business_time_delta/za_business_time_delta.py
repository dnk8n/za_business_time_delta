from datetime import datetime, time, timedelta
import re

import holidays
import pytz

UNCONVERTED_DATA_REMAINS_REGEX = re.compile(r'^unconverted data remains: (\d+)?([-+]\d{2}:?\d{0,2})?$')


def get_iso8601_datetime(time_string: str) -> datetime:
    """
    One can't be certain on time format coming in. ISO 8601 can have many forms. This function attempts to support
    the most common ones.
    """
    # Necessary to recognise time strings ending with Z as UTC
    reformatted_time_string = time_string.replace('Z', '+0000')
    # Todo: Generate these formats programmatically
    # Todo: To be fully ISO 8601 compliant, decimal points/commas should be supported at each lowest level,
    #       e.g 2020-01-01T13.5; 2020-01-01T13:30.5; 2020-01-01T13:30:30.5
    #       This is not supported
    for fmt in ('%G-W%V-%uT%H:%M',
                '%G-W%V-%uT%H:%M:%S',
                '%G-W%V-%uT%H:%M:%S.%f',
                '%GW%V%uT%H%M',
                '%GW%V%uT%H%M%S',
                '%GW%V%uT%H%M%S.%f',
                '%Y-%jT%H:%M',
                '%Y-%jT%H:%M:%S',
                '%Y-%jT%H:%M:%S.%f',
                '%Y%jT%H%M',
                '%Y%jT%H%M%S',
                '%Y%jT%H%M%S.%f',
                '%Y-%m-%dT%H:%M',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y%m%dT%H%M',
                '%Y%m%dT%H%M%S',
                '%Y%m%dT%H%M%S.%f'):
        try:
            # For each format, try cast to datetime. If it succeeds it is the datetime wanted
            return datetime.strptime(reformatted_time_string, fmt)
        except ValueError as e:
            uncovered_data = UNCONVERTED_DATA_REMAINS_REGEX.search(str(e))
            # Two reasons for uncovered data, UCT offset and/or more than 6 digits in fraction
            if uncovered_data:
                extra_digits = uncovered_data.group(1)
                uct_offset = uncovered_data.group(2)
                fixed_uct_offset = ''
                if uct_offset:
                    # Note bugs: https://bugs.python.org/issue15873, https://bugs.python.org/issue31800 which means that
                    # UTC offset is not recognised when for e.g. in format +04:00 instead of +0400. This is fixed in
                    # Python 3.7 but we want to support Python 3.6, therefore strip final colon.
                    reformatted_time_string = reformatted_time_string.replace(uct_offset, '')
                    # Ensure of format +0400 for example
                    fixed_uct_offset = uct_offset.replace(':', '').ljust(5, '0')
                if '%f' in fmt and extra_digits:
                    # Strip extra digits from fraction because only 6 are supported by strptime's %f
                    reformatted_time_string = re.sub(rf'{extra_digits}$', '', reformatted_time_string)
                if uct_offset:
                    # Add fixed UTC offset back to string
                    reformatted_time_string += fixed_uct_offset
                    # Modify strptime format to take UTC offset into account
                    fmt = fmt + '%z'
                if uct_offset or ('%f' in fmt and extra_digits):
                    # If either of the above uncovered data conditions occurred, return according to new format
                    try:
                        return datetime.strptime(reformatted_time_string, fmt)
                    except ValueError:
                        pass
    raise ValueError(f'{time_string} does not conform to an ISO 8601 compatible format.')


def get_time_delta(start_time: str, end_time: str) -> int:
    """
    This function inputs 2 parameters, start time and end time, and outputs an integer of business seconds, where a
    business second is a second between 08:00 and 17:00 Monday to Friday, not including a public holiday in the
    Republic of South Africa.

    >>> get_time_delta('2020-02-04T07:36:12+00:00', '2020-02-04T07:36:22+00:00')
    10
    >>> get_time_delta('2020-02-04T07:36:22+01:00', '2020-02-04T07:36:12+00:00')
    3590
    >>> get_time_delta('2020-02-04T07:36:12+00:00', '2020-02-04T07:36:22-01:00')
    3610
    >>> get_time_delta('2020-02-04T07:36:12Z', '2020-02-04T07:36:22Z')
    10
    >>> get_time_delta('20200204T073612Z', '20200204T073622Z')
    10
    """
    start_datetime = get_iso8601_datetime(start_time)
    end_datetime = get_iso8601_datetime(end_time)

    # Todo: Current implementation could do with improvement in terms of efficiency. With that in mind, for now, we are
    #       going to limit max time delta to an arbitrary 40,000 days, else request time will likely be too slow.
    day_delta = (end_datetime - start_datetime).days
    if day_delta > 40000:
        raise ValueError(f'Time delta of {day_delta} days, exceeds 40000 days that is currently supported. Please '
                         f'try again with shorter time delta.')

    # Convert into South African Standard Time (SAST) so that we can check hours against 8 or 17 (start/end of workday)
    za_start_datetime = start_datetime.astimezone(pytz.timezone('Africa/Johannesburg'))
    za_end_datetime = end_datetime.astimezone(pytz.timezone('Africa/Johannesburg'))

    this_za_datetime = za_start_datetime
    one_day = timedelta(days=1)
    business_seconds = 0
    za_holidays = holidays.SouthAfrica()
    while this_za_datetime <= za_end_datetime:
        #
        # print(this_za_datetime, za_end_datetime, business_seconds)
        #
        if this_za_datetime.date() in za_holidays:
            #
            # print('Holiday')
            #
            pass
        elif this_za_datetime.weekday() > 4:
            #
            # print('Weekend')
            #
            pass
        else:
            #
            # print('Business Day')
            #
            if this_za_datetime.time() < time(8, 0, 0):
                #
                # print('Before Hours')
                #
                if za_end_datetime.date() == this_za_datetime.date():
                    if za_end_datetime.time() < time(8, 0, 0):
                        #
                        # print('No Business day ahead')
                        #
                        pass
                    elif za_end_datetime.time() > time(17, 0, 0):
                        #
                        # print('Full Business day ahead')
                        #
                        business_seconds += ((17 - 8) * 60 * 60)
                    else:
                        #
                        # print('Part Business day ahead')
                        #
                        business_seconds += (int((za_end_datetime - this_za_datetime).total_seconds()))
                else:
                    #
                    # print('Full Business day ahead')
                    #
                    business_seconds += ((17 - 8) * 60 * 60)
            elif this_za_datetime.time() > time(17, 0, 0):
                #
                # print('After Hours')
                #
                pass
            else:
                #
                # print('Business Hours')
                #
                if za_end_datetime.date() == this_za_datetime.date():
                    if za_end_datetime.time() > time(17, 0, 0):
                        #
                        # print('Time difference between start time and 17:00')
                        #
                        business_seconds += int((za_end_datetime.replace(hour=17, minute=0, second=0, microsecond=0) - this_za_datetime).total_seconds())
                    else:
                        #
                        # print('Time difference between start time and end time')
                        #
                        business_seconds += (int((za_end_datetime - this_za_datetime).total_seconds()))
                else:
                    if this_za_datetime.time() < time(8, 0, 0):
                        #
                        # print('Full Business day ahead')
                        #
                        business_seconds += ((17 - 8) * 60 * 60)
                    elif this_za_datetime.time() > time(17, 0, 0):
                        #
                        # print('No Business day ahead')
                        #
                        pass
                    else:
                        #
                        # print('Part Business day ahead')
                        #
                        business_seconds += (int((this_za_datetime.replace(hour=17, minute=0, second=0, microsecond=0) - this_za_datetime).total_seconds()))
        this_za_datetime += one_day
    return business_seconds

