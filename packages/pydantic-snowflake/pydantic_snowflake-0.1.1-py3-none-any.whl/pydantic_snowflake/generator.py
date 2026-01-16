from datetime import datetime, timezone

try:
    from datetime import UTC  # type: ignore
except ImportError:
    from datetime import timezone
    UTC = timezone.utc

from .const import (
    DEFAULT_EPOCH_TS,
    TS_OFFSET,
    WORK_OFFSET,
    WORK_MASK,
    PROC_OFFSET,
    PROC_MASK,
    SEQ_MASK,
)
from .snowflake import SnowflakeId

STARTUP_DATETIME = datetime.now(UTC)


class SnowflakeGenerator():
    """
    A Snowflake ID generator class.
    """
    _last_timestamp: int
    _epoch: datetime
    _worker: int
    _process: int
    _sequence: int

    def __init__(
        self,
        epoch: datetime = DEFAULT_EPOCH_TS,
        worker_id: int = 0,
        process_id: int = 0,
    ):
        """
        :param epoch: The epoch datetime for timestamp calculation.
        :type epoch: datetime
        :param worker_id: The worker ID.
        :type worker_id: int
        :param process_id: The process ID.
        :type process_id: int
        """
        if worker_id < 0 or worker_id > WORK_MASK:
            raise ValueError(f"worker_id must be between 0 and {WORK_MASK}")
        if process_id < 0 or process_id > PROC_MASK:
            raise ValueError(f"process_id must be between 0 and {PROC_MASK}")

        self._last_timestamp = 0
        self._epoch = epoch.astimezone(UTC)
        self._worker = worker_id
        self._process = process_id
        self._sequence = 0

        now_datetime = datetime.now(UTC)
        if now_datetime < STARTUP_DATETIME:
            raise ValueError("System clock moved backwards.")

        if (now_datetime - self._epoch).total_seconds() < 0:
            raise ValueError("Epoch is set in the future.")

        while (now_datetime - STARTUP_DATETIME).total_seconds() < 0.001:
            now_datetime = datetime.now(UTC)

    def __iter__(self):
        return self

    def __next__(self) -> SnowflakeId:
        delta = (datetime.now(UTC) - self._epoch)
        current = int(delta.total_seconds() * 1000)

        if current == self._last_timestamp:
            if self._sequence < SEQ_MASK:
                self._sequence += 1
            else:
                while current != self._last_timestamp:
                    delta = (datetime.now(UTC) - self._epoch)
                    current = int(delta.total_seconds() * 1000)
                self._sequence = 0
        else:
            self._sequence = 0

        self._last_timestamp = current

        value = (current << TS_OFFSET)
        value |= self._worker << WORK_OFFSET
        value |= self._process << PROC_OFFSET
        value |= self._sequence

        return SnowflakeId(value=value, epoch=self._epoch)

    def next(self) -> SnowflakeId:
        """
        Generate the next Snowflake ID.

        :return: The next Snowflake ID.
        :rtype: SnowflakeId
        """
        return self.__next__()
