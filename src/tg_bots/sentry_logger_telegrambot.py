import logging
import traceback
from functools import wraps

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.WARNING
)

sentry_sdk.init(
    dsn="https://74006656885b4d008f2fabc54a71a54c@o4504847855386624.ingest.sentry.io/4504867212427264",
    integrations=[
        sentry_logging
    ],
)


def logging_func(logger):
    def logger_func(function):
        @wraps(function)
        def inner(*args):
            try:
                logging.info(f'Function is started in {function.__name__}')
                function(*args)
            except (Exception,):
                logging.exception(f'Exception is occurred in {function.__name__}, {traceback.format_exc()}')

        return inner

    return logger_func




