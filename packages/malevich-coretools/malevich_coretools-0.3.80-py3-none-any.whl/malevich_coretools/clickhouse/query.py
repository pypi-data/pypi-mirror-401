from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from malevich_coretools.clickhouse.abstract import Table

Direction = Literal['asc', 'desc']


class Options(BaseModel):
    orderByColumn: Optional[str] = None
    orderByDirection: Direction = 'asc'
    limit: Optional[int] = None
    offset: Optional[int] = None


class FiltersNode(BaseModel):
    type: str


class FiltersNodeOr(FiltersNode):
    type: Literal['or'] = 'or'
    data: List['FilterNodeType']

    def __repr__(self) -> str:
        return f"Or{self.data}"

    __str__ = __repr__


class FiltersNodeAnd(FiltersNode):
    type: Literal['and'] = 'and'
    data: List['FilterNodeType']

    def __repr__(self) -> str:
        return f"And{self.data}"

    __str__ = __repr__


class FiltersLeaf(FiltersNode):
    type: Literal['leaf'] = 'leaf'
    eq: Optional[Dict[str, Union[str, int, float, bool]]] = None
    neq: Optional[Dict[str, Union[str, int, float, bool]]] = None
    gt: Optional[Dict[str, Union[str, int, float, bool]]] = None
    gte: Optional[Dict[str, Union[str, int, float, bool]]] = None
    lt: Optional[Dict[str, Union[str, int, float, bool]]] = None
    lte: Optional[Dict[str, Union[str, int, float, bool]]] = None
    contains: Optional[Dict[str, str]] = None
    notContains: Optional[Dict[str, str]] = None
    in_: Optional[Dict[str, List[str]]] = Field(alias="in", default=None)
    notIn: Optional[Dict[str, List[str]]] = None
    like: Optional[Dict[str, str]] = None
    notLike: Optional[Dict[str, str]] = None

    model_config = ConfigDict(serialize_by_alias=True)

    def __repr__(self) -> str:
        res = self.model_dump(exclude_none=True)
        res.pop("type")
        return f"Leaf{res}"

    __str__ = __repr__


FilterNodeType = Union[FiltersNodeOr, FiltersNodeAnd, FiltersLeaf]
FiltersNodeOr.model_rebuild()
FiltersNodeAnd.model_rebuild()


class ClickhouseQuery(BaseModel):
    operationIds: List[str] = []    # empty - all
    runIds: List[str] = []          # empty - all
    table: Table
    filters: Optional[FilterNodeType] = None
    options: Options = Options()
