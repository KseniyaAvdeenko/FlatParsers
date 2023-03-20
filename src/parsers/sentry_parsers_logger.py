import functools
import logging
import traceback

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.INFO
)

sentry_sdk.init(
    dsn="https://c98a1a22b0cb45049b77580bebbc15b9@o4504847855386624.ingest.sentry.io/4504867476013056",
    integrations=[
        sentry_logging
    ]
)


def logging_func(logger):
    def logger_func(function):
        @functools.wraps(function)
        def inner(*args, **kwargs):
            try:
                logging.info(f'Function is started {function}')
                function(*args, **kwargs)
            except (Exception,):
                logging.exception(f'Exception is occurred in {function}', {traceback.format_exc()})

            return inner
        return logger_func

