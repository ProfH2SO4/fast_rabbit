import enum


class RequestStatus(enum.IntEnum):
    """
    If message was successfully processed and send to client or not.
    Can be distinguished if message is needed to be acked.
    """

    OK = 1
    FAILED = 2
