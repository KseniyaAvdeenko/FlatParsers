import logging
import traceback

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import functools

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.INFO
)

sentry_sdk.init(
    dsn="https://0d5c4da433d647e39fc3fa0362683446@o4504847855386624.ingest.sentry.io/4504867484336128",
    integrations=[
        sentry_logging
    ]
)


def logging_func(logger):
    def logger_func(function):
        @functools.wraps(function)
        def inner():
            try:
                logging.info(f'Function is started in {function.__name__}')
                function()
            except (Exception,):
                logging.exception(f'Exception is occurred in {function.__name__}, {traceback.format_exc()}')

        return inner

    return logger_func


