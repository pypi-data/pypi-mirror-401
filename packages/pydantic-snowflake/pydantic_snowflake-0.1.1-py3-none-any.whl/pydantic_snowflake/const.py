from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

from datetime import datetime, timedelta
from typing import Any, Union

try:
    from datetime import UTC  # type: ignore
except ImportError:
    from datetime import timezone
    UTC = timezone.utc

DEFAULT_EPOCH_TS = datetime(
    year=2015,
    month=1,
    day=1,
    tzinfo=UTC
)

TS_LEN = 42
WORK_ID_LEN = 5
PROC_ID_LEN = 5
SEQ_LEN = 12

TS_OFFSET = 22
WORK_OFFSET = 17
PROC_OFFSET = 12

WORK_MASK = (1 << WORK_ID_LEN) - 1
PROC_MASK = (1 << PROC_ID_LEN) - 1
SEQ_MASK = (1 << SEQ_LEN) - 1
