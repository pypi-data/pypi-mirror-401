from typing import List, Literal

from pydantic import BaseModel


class ClickhouseCfgRecord(BaseModel):
    cfgId: str
    data: str
    operationId: str
    id: str


class ClickhouseCollectionRecord(BaseModel):
    runId: str
    collectionId: str
    schemeId: str
    groupName: str
    index: int
    operationId: str
    id: str


class ClickhouseFunRecord(BaseModel):
    timestampStart: str
    timestampEnd: str
    runId: str
    bindId: str
    iteration: int
    funId: str
    success: bool
    inside: bool
    operationId: str
    id: str


class ClickhouseLogRecord(BaseModel):
    runId: str
    bindId: str
    funId: str
    scale: int
    data: str
    type: Literal['LOGS', 'LOGS_USER', 'LOGS_OPERATION', 'ERROR']
    operationId: str
    id: str


class ClickhouseOperationRecord(BaseModel):
    prepareTimestampStart: str
    prepareTimestampEnd: str
    imageUrls: List[str]
    pipelineId: str
    cfgId: str
    operationId: str
    id: str


class ClickhouseRunRecord(BaseModel):
    timestampStart: str
    timestampEnd: str
    runId: str
    cfgId: str
    dagLogs: str
    success: bool
    operationId: str
    id: str
