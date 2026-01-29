from typing import Any, Callable, Coroutine, List, Literal, Optional, Union, overload

import malevich_coretools.funcs.funcs as f
from malevich_coretools.abstract import AUTH
from malevich_coretools.abstract.clickhouse import (
    ClickhouseCfgRecord,
    ClickhouseCollectionRecord,
    ClickhouseFunRecord,
    ClickhouseLogRecord,
    ClickhouseOperationRecord,
    ClickhouseRunRecord,
)
from malevich_coretools.batch import Batcher
from malevich_coretools.clickhouse.abstract import (
    ClickhouseCfg,
    ClickhouseCollection,
    ClickhouseFun,
    ClickhouseLog,
    ClickhouseOperation,
    ClickhouseRun,
)
from malevich_coretools.clickhouse.query import ClickhouseQuery, Options
from malevich_coretools.clickhouse.where_utils import BM, where
from malevich_coretools.secondary import Config


@overload
def clickhouse_query(
    model: type[ClickhouseCfg],
    condition_builder: Callable[[ClickhouseCfg], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[False] = False,
) -> List[ClickhouseCfgRecord]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseCollection],
    condition_builder: Callable[[ClickhouseCollection], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[False] = False,
) -> List[ClickhouseCollectionRecord]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseFun],
    condition_builder: Callable[[ClickhouseFun], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[False] = False,
) -> List[ClickhouseFunRecord]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseLog],
    condition_builder: Callable[[ClickhouseLog], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[False] = False,
) -> List[ClickhouseLogRecord]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseOperation],
    condition_builder: Callable[[ClickhouseOperation], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[False] = False,
) -> List[ClickhouseOperationRecord]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseRun],
    condition_builder: Callable[[ClickhouseRun], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[False] = False,
) -> List[ClickhouseRunRecord]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseCfg],
    condition_builder: Callable[[ClickhouseCfg], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[True],
) -> Coroutine[Any, Any, List[ClickhouseCfgRecord]]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseCollection],
    condition_builder: Callable[[ClickhouseCollection], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[True],
) -> Coroutine[Any, Any, List[ClickhouseCollectionRecord]]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseFun],
    condition_builder: Callable[[ClickhouseFun], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[True],
) -> Coroutine[Any, Any, List[ClickhouseFunRecord]]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseLog],
    condition_builder: Callable[[ClickhouseLog], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[True],
) -> Coroutine[Any, Any, List[ClickhouseLogRecord]]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseOperation],
    condition_builder: Callable[[ClickhouseOperation], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[True],
) -> Coroutine[Any, Any, List[ClickhouseOperationRecord]]:
    pass


@overload
def clickhouse_query(
    model: type[ClickhouseRun],
    condition_builder: Callable[[ClickhouseRun], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: Literal[True],
) -> Coroutine[Any, Any, List[ClickhouseRunRecord]]:
    pass


def clickhouse_query(
    model: type[BM],    # ClickhouseModel
    condition_builder: Callable[[BM], bool],
    operation_ids: Optional[List[str]] = None,
    run_ids: Optional[List[str]] = None,
    options: Optional[Options] = None,
    wait: bool = True,
    *,
    auth: Optional[AUTH] = None,
    conn_url: Optional[str] = None,
    batcher: Optional[Batcher] = None,
    is_async: bool = False,
) -> Union[ClickhouseCfgRecord, ClickhouseCollectionRecord, ClickhouseFunRecord, ClickhouseLogRecord, ClickhouseOperationRecord, ClickhouseRunRecord, Coroutine[Any, Any, Union[ClickhouseCfgRecord, ClickhouseCollectionRecord, ClickhouseFunRecord, ClickhouseLogRecord, ClickhouseOperationRecord, ClickhouseRunRecord]]]:
    """return clickhouse response, if ids is None - find for all, model - ClickhouseModel"""
    if batcher is None:
        batcher = Config.BATCHER
    data = ClickhouseQuery(
        operationIds=operation_ids or [],
        runIds=run_ids or [],
        table=model.table(),
        filters=where(model, condition_builder),
        options=Options() if options is None else options
    )
    model = model.recordClass()
    if batcher is not None:
        return batcher.add("clickhouseQuery", data=data, result_model=List[model])
    if is_async:
        return f.post_clickhouse_query_async(data, model=model, wait=wait, auth=auth, conn_url=conn_url)
    return f.post_clickhouse_query(data, model=model, wait=wait, auth=auth, conn_url=conn_url)
