"""
amochka: Библиотека для работы с API amoCRM.
"""

__version__ = "0.4.4"

from .client import AmoCRMClient, CacheConfig
from .errors import (
    AmoCRMError,
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from .etl import (
    write_ndjson,
    export_leads_to_ndjson,
    export_contacts_to_ndjson,
    export_notes_to_ndjson,
    export_events_to_ndjson,
    export_users_to_ndjson,
    export_pipelines_to_ndjson,
)

__all__ = [
    "AmoCRMClient",
    "CacheConfig",
    # Exceptions
    "AmoCRMError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    # ETL functions
    "write_ndjson",
    "export_leads_to_ndjson",
    "export_contacts_to_ndjson",
    "export_notes_to_ndjson",
    "export_events_to_ndjson",
    "export_users_to_ndjson",
    "export_pipelines_to_ndjson",
]
