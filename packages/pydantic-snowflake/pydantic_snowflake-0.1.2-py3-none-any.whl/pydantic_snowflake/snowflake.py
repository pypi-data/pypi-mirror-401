from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

from typing import Any, Union
from datetime import datetime as sys_datetime, timezone, timedelta

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


class SnowflakeId():
    """
    A Snowflake ID representation class for Pydantic models.

    :var value: Snowflake ID's integer value
    :vartype value: int
    :var epoch: Epoch datetime used for timestamp calculation
    :vartype epoch: datetime
    """
    value: int
    epoch: sys_datetime

    def __init__(self, value: Union[int, str], epoch: sys_datetime = DEFAULT_EPOCH_TS) -> None:
        """
        :param value: The Snowflake ID value.
        :type value: Union[int, str]
        :param epoch: The epoch datetime for timestamp calculation.
        :type epoch: datetime
        """
        self.epoch = epoch.astimezone(UTC)

        if isinstance(value, int):
            self.value = value
            return

        try:
            self.value = int(value)
        except ValueError as e:
            raise ValueError(f"Invalid Snowflake ID string: {value}") from e

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"<SnowflakeId value={self.value}>"

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, self.__class__):
            return self.value == obj.value

        if isinstance(obj, int):
            return self.value == obj

        try:
            other_value = int(obj)  # type: ignore
            return self.value == other_value
        except:
            return False

    def __hash__(self) -> int:
        return self.value

    @property
    def datetime(self) -> sys_datetime:
        """
        :return: The datetime representation of the Snowflake ID.
        :rtype: datetime
        """
        mill_seconds = (self.value >> TS_OFFSET) % 1000
        delta_seconds = (self.value >> TS_OFFSET) // 1000

        return self.epoch + timedelta(
            seconds=delta_seconds,
            milliseconds=mill_seconds
        )

    @property
    def timestamp(self) -> float:
        """
        :return: The timestamp representation of the Snowflake ID.
        :rtype: float
        """
        dt = self.datetime
        return dt.timestamp()

    @property
    def worker_id(self) -> int:
        """
        :return: The worker ID extracted from the Snowflake ID.
        :rtype: int
        """
        return (self.value >> WORK_OFFSET) & WORK_MASK

    @property
    def process_id(self) -> int:
        """
        :return: The process ID extracted from the Snowflake ID.
        :rtype: int
        """
        return (self.value >> PROC_OFFSET) & PROC_MASK

    @property
    def sequence(self) -> int:
        """
        :return: The sequence number extracted from the Snowflake ID.
        :rtype: int
        """
        return self.value & SEQ_MASK

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema["type"] = "string"
        json_schema["examples"] = ["6209533852516352"]
        json_schema["title"] = "SnowflakeId"
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        def from_string(value: Any) -> SnowflakeId:
            if isinstance(value, SnowflakeId):
                return value
            try:
                return SnowflakeId(value=value)
            except ValueError:
                raise ValueError(f"Invalid value for SnowflakeId: {value}")

        def to_string(value: SnowflakeId) -> str:
            return str(value.value)

        return core_schema.json_or_python_schema(
            json_schema=core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_before_validator_function(
                    from_string,
                    core_schema.any_schema()
                )
            ]),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(cls),
                core_schema.int_schema(),
                core_schema.str_schema(),
                core_schema.no_info_before_validator_function(
                    from_string,
                    core_schema.any_schema()
                )
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                to_string,
                return_schema=core_schema.str_schema(),
                when_used="json"
            )
        )
