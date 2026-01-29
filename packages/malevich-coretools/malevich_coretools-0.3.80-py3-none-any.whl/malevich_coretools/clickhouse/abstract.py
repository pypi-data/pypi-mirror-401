from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Generic, List, Literal, Type, TypeVar

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import core_schema

from malevich_coretools.abstract.clickhouse import (
    ClickhouseCfgRecord,
    ClickhouseCollectionRecord,
    ClickhouseFunRecord,
    ClickhouseLogRecord,
    ClickhouseOperationRecord,
    ClickhouseRunRecord,
)

T = TypeVar('T')


class AnyField(Generic[T]):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,    # noqa: ANN102
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        origin = getattr(source_type, '__origin__', None)
        args = getattr(source_type, '__args__', ())

        if origin is BaseField and args:
            inner_schema = handler.generate_schema(args[0])
            return inner_schema

        return core_schema.any_schema()

class InField(Generic[T], AnyField[T]):
    def in_(self, value: List[T]) -> bool: pass
    def not_in(self, value: List[T]) -> bool: pass

class BaseField(Generic[T], InField[T]):
    def __ne__(self, value: T) -> bool: pass
    def __eq__(self, value: T) -> bool: pass

class CompareField(Generic[T], BaseField[T]):
    def __gt__(self, value: T) -> bool: pass
    def __ge__(self, value: T) -> bool: pass
    def __lt__(self, value: T) -> bool: pass
    def __le__(self, value: T) -> bool: pass

class LikeField(Generic[T], AnyField[T]):
    def __contains__(self, value: T) -> bool: pass
    def contains(self, value: T) -> bool: pass
    def not_contains(self, value: T) -> bool: pass
    def like(self, value: T) -> bool: pass
    def not_like(self, value: T) -> bool: pass


class StringIdField(BaseField[str]):
    pass

class StringIdExtendedField(BaseField[str], LikeField[str]):
    pass

class StringField(CompareField[str], LikeField[str]):
    pass

class DateField(CompareField[datetime]):
    pass

class NumField(Generic[T], CompareField[T]):
    pass

class BoolField(Generic[T], BaseField[T]):
    pass

class EnumField(Generic[T], BaseField[T]):
    pass

class ListStringField(InField[str]):
    pass


Table = Literal['cfg', 'collection', 'fun', 'log', 'operation', 'run']


class ClickhouseModel(BaseModel, ABC):
    @abstractmethod
    def table() -> Table:
        pass

    @abstractmethod
    def recordClass() -> Type[BaseModel]:
        pass


class ClickhouseCfg(ClickhouseModel):
    cfgId: StringField
    data: StringField
    operationId: StringIdField
    id: StringIdField

    def table() -> Table:
        return 'cfg'

    def recordClass() -> Type[BaseModel]:
        return ClickhouseCfgRecord


class ClickhouseCollection(ClickhouseModel):
    runId: StringIdExtendedField
    collectionId: StringIdField
    schemeId: StringIdField
    groupName: StringField
    index: NumField[int]
    operationId: StringIdField
    id: StringIdField

    def table() -> Table:
        return 'collection'

    def recordClass() -> Type[BaseModel]:
        return ClickhouseCollectionRecord


class ClickhouseFun(ClickhouseModel):
    timestampStart: DateField
    timestampEnd: DateField
    ts: NumField[float]     # diff between timestamps
    runId: StringIdExtendedField
    bindId: StringField
    iteration: NumField[int]
    funId: StringField
    success: BoolField
    inside: BoolField
    operationId: StringIdField
    id: StringIdField

    def table() -> Table:
        return 'fun'

    def recordClass() -> Type[BaseModel]:
        return ClickhouseFunRecord


class ClickhouseLog(ClickhouseModel):
    runId: StringIdExtendedField
    bindId: StringField
    funId: StringField
    scale: NumField[int]
    data: StringField
    type: EnumField[Literal['LOGS', 'LOGS_USER', 'LOGS_OPERATION', 'ERROR']]
    operationId: StringIdField
    id: StringIdField

    def table() -> Table:
        return 'log'

    def recordClass() -> Type[BaseModel]:
        return ClickhouseLogRecord


class ClickhouseOperation(ClickhouseModel):
    prepareTimestampStart: DateField
    prepareTimestampEnd: DateField
    ts: NumField[float]     # diff between timestamps
    imageUrls: ListStringField
    pipelineId: StringField
    cfgId: StringField
    operationId: StringIdField
    id: StringIdField

    def table() -> Table:
        return 'operation'

    def recordClass() -> Type[BaseModel]:
        return ClickhouseOperationRecord


class ClickhouseRun(ClickhouseModel):
    timestampStart: DateField
    timestampEnd: DateField
    ts: NumField[float]     # diff between timestamps
    runId: StringIdExtendedField
    cfgId: StringField
    dagLogs: StringField
    success: BoolField
    operationId: StringIdField
    id: StringIdField

    def table() -> Table:
        return 'run'

    def recordClass() -> Type[BaseModel]:
        return ClickhouseRunRecord
