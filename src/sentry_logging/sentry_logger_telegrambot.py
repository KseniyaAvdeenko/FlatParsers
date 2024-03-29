import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from src.sentry_logging.base_logging import *

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.INFO
)

sentry_sdk.init(
    dsn="https://74006656885b4d008f2fabc54a71a54c@o4504847855386624.ingest.sentry.io/4504867212427264",
    integrations=[
        sentry_logging
    ],
)
