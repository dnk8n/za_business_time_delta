def get_time_delta(start_time: str, end_time: str) -> int:
    """
    This function inputs 2 parameters, start time and end time, and outputs an integer of business seconds, where a
    business second is a second between 08:00 and 17:00 Monday to Friday, not including a public holiday in the
    Republic of South Africa.

    >>> get_time_delta('2020-02-04T07:36:12+00:00', '2020-02-01T07:36:22+00:00')
    10
    >>> get_time_delta('2020-02-04T07:36:12+00:00', '2020-02-01T07:36:22+01:00') # TODO: Check I have this right
    3610
    >>> get_time_delta('2020-02-04T07:36:12Z', '2020-02-01T07:36:22Z')
    10
    >>> get_time_delta('20200204T073612Z', '20200201T073622Z')
    10
    """
    # Todo: Implement this function: Right now this is just a mock/skeleton to test that deployments are working
    return int(end_time) - int(start_time)
