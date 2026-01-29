from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from pydantic import BaseModel, ConfigDict

from malevich_coretools.clickhouse.abstract import ClickhouseModel
from malevich_coretools.clickhouse.query import (
    FilterNodeType,
    FiltersLeaf,
    FiltersNodeAnd,
    FiltersNodeOr,
)

BM = TypeVar('BM', bound=ClickhouseModel)


class OperationType(Enum):
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    Contains = "contains"
    NotContains = "notContains"
    IN = "in"
    NotIN = "notIn"
    Like = "like"
    NotLike = "notLike"

_operation_type_inverse_mapping = {
    OperationType.EQ: OperationType.NEQ,
    OperationType.NEQ: OperationType.EQ,
    OperationType.GT: OperationType.LTE,
    OperationType.GTE: OperationType.LT,
    OperationType.LT: OperationType.GTE,
    OperationType.LTE: OperationType.GT,
    OperationType.Contains: OperationType.NotContains,
    OperationType.NotContains: OperationType.Contains,
    OperationType.IN: OperationType.NotIN,
    OperationType.NotIN: OperationType.IN,
    OperationType.Like: OperationType.NotLike,
    OperationType.NotLike: OperationType.Like
}


class Condition:
    def __init__(self) -> None:
        self.op: Optional[OperationType] = None
        self.key: Optional[str] = None
        self.value: Optional[Any] = None
        self.or_conds: Optional[Tuple[Condition, Condition]] = None
        self.and_conds: Optional[Tuple[Condition, Condition]] = None
        self.inverse: bool = False

    @staticmethod
    def operation(op: OperationType, key: str, value: Any) -> 'Condition':
        cond = Condition()
        cond.op = op
        cond.key = key
        cond.value = value
        return cond

    def __and__(self, other: 'Condition') -> 'Condition':
        cond = Condition()
        cond.and_conds = (self, other)
        return cond

    def __or__(self, other: 'Condition') -> 'Condition':
        cond = Condition()
        cond.or_conds = (self, other)
        return cond

    def __invert__(self) -> None:
        self.inverse ^= True
        return self

    def __repr__(self) -> str:
        if self.op is not None:
            return f"({self.key} {self.op.value} {self.value})"
        elif self.and_conds is not None:
            return f"And{self.and_conds}"
        elif self.or_conds is not None:
            return f"Or{self.or_conds}"
        else:
            return "Condition"

    __str__ = __repr__

    @overload
    def compile(self, inside: Literal[False] = False) -> FilterNodeType:
        pass

    @overload
    def compile(self, inside: Literal[True]) -> Union[FilterNodeType, Dict]:
        pass

    def compile(self, inside: bool = False) -> Union[FilterNodeType, Dict]:
        if self.op is not None:
            if self.inverse:
                self.op = _operation_type_inverse_mapping[self.op]

            if isinstance(self.value, datetime):
                self.value = self.value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            res = {self.op.value: {self.key: self.value}}
            if not inside:
                res = FiltersLeaf(**res)
            return res
        elif self.and_conds is not None:
            if self.inverse:
                self.and_conds[0].inverse ^= True
                self.and_conds[1].inverse ^= True
                self.or_conds, self.and_conds = self.and_conds, None
                self.inverse = False
                return self.compile(inside=inside)

            res = self.and_conds[0].compile(inside=True)
            res2 = self.and_conds[1].compile(inside=True)

            if not isinstance(res, dict) and isinstance(res2, dict):
                res2, res = res, res2

            if isinstance(res, dict):
                if isinstance(res2, dict):
                    res_secondary = {}
                    for op, values in res.items():
                        if (values2 := res2.pop(op, None)) is not None:
                            values_secondary = {}
                            for name, value2 in values2.items():
                                if (value := values.get(name)) is not None:
                                    if value != value2:
                                        values_secondary[name] = value2
                                else:
                                    values[name] = value2
                            if len(values_secondary) > 0:
                                res_secondary[op] = values_secondary
                    for op, values in res2.items():
                        res[op] = values
                    if len(res_secondary) > 0:
                        res = FiltersNodeAnd(data=[FiltersLeaf(**res), FiltersLeaf(**res_secondary)])
                    elif not inside:
                        res = FiltersLeaf(**res)
                    return res
                res = FiltersLeaf(**res)
                if isinstance(res2, FiltersNodeAnd):
                    return res2.data.append(res)
                else:   # FiltersNodeOr
                    return FiltersNodeAnd(data=[res, res2])
            else:
                if isinstance(res, FiltersNodeAnd):
                    if isinstance(res2, FiltersNodeAnd):
                        res.data.extend(res2.data)
                    else:
                        res.data.append(res2)
                    return res
                elif isinstance(res2, FiltersNodeAnd):
                    res2.data.append(res)
                    return res2
                else:
                    return FiltersNodeAnd(data=[res, res2])
        elif self.or_conds is not None:
            if self.inverse:
                self.or_conds[0].inverse ^= True
                self.or_conds[1].inverse ^= True
                self.and_conds, self.or_conds = self.or_conds, None
                self.inverse = False
                return self.compile(inside=inside)

            res = self.or_conds[0].compile()
            res2 = self.or_conds[1].compile()

            if isinstance(res, FiltersNodeOr):
                if isinstance(res2, FiltersNodeOr):
                    res.data.extend(res2.data)
                else:
                    res.data.append(res2)
                return res
            elif isinstance(res2, FiltersNodeOr):
                res2.data.append(res)
                return res2
            else:
                return FiltersNodeOr(data=[res, res2])
        else:
            raise Exception("empty condition")


class FieldExpression:
    def __init__(self, key: str) -> None:
        self.key = key

    def __eq__(self, value: Any) -> Condition:
        return Condition.operation(OperationType.EQ, self.key, value)

    def __ne__(self, value: Any) -> Condition:
        return Condition.operation(OperationType.NEQ, self.key, value)

    def __gt__(self, value: Any) -> Condition:
        return Condition.operation(OperationType.GT, self.key, value)

    def __ge__(self, value: Any) -> Condition:
        return Condition.operation(OperationType.GTE, self.key, value)

    def __lt__(self, value: Any) -> Condition:
        return Condition.operation(OperationType.LT, self.key, value)

    def __le__(self, value: Any) -> Condition:
        return Condition.operation(OperationType.LTE, self.key, value)

    def __contains__(self, value: Any) -> Condition:
        return Condition.operation(OperationType.Contains, self.key, value)

    def contains(self, value: Any) -> Condition:
        return Condition.operation(OperationType.Contains, self.key, value)

    def not_contains(self, value: Any) -> Condition:
        return Condition.operation(OperationType.NotContains, self.key, value)

    def in_(self, value: List[Any]) -> Condition:
        return Condition.operation(OperationType.IN, self.key, value)

    def not_in(self, value: List[Any]) -> Condition:
        return Condition.operation(OperationType.NotIN, self.key, value)

    def like(self, value: Any) -> Condition:
        return Condition.operation(OperationType.Like, self.key, value)

    def not_like(self, value: Any) -> Condition:
        return Condition.operation(OperationType.NotLike, self.key, value)


def _create_query_model(base_model: type[BM]) -> type[BM]:
    class QueryModel(BaseModel):
        model_config = ConfigDict(extra='allow')

        def __init__(self, **kwargs) -> None:
            super().__init__()

        def __getattr__(self, name: str) -> FieldExpression:
            if name not in base_model.model_fields:
                raise AttributeError(f"{base_model.__name__} has no field \"{name}\"")
            return FieldExpression(name)
    QueryModel.__name__ = f"Query{base_model.__name__}"
    return QueryModel


def where(
    model: type[BM],
    condition_builder: Callable[[BM], bool]
) -> FilterNodeType:
    query_model = _create_query_model(model)
    instance = query_model()
    condition: Condition = condition_builder(instance)
    return condition.compile()
