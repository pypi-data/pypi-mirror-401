import logging
import re

PHONE_REGEX = r"\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b"
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class PIIFilter(logging.Filter):
    """
    Log filter that masks Emails and Phone numbers in log messages.
    """

    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = re.sub(EMAIL_REGEX, "[EMAIL_REDACTED]", record.msg)
            record.msg = re.sub(PHONE_REGEX, "[PHONE_REDACTED]", record.msg)
        return True
