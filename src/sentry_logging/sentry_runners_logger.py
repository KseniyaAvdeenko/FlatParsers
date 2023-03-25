import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

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
