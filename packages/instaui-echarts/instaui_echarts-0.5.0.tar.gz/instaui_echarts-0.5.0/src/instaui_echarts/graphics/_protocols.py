from typing import Protocol, Iterable, Union, runtime_checkable


# region pandas protocol


@runtime_checkable
class PandasDataFrameValuesProtocol(Protocol):
    def tolist(self) -> list: ...


@runtime_checkable
class PandasDataFrameProtocol(Protocol):
    @property
    def columns(self) -> Iterable[str]: ...

    @property
    def values(self) -> PandasDataFrameValuesProtocol: ...


# endregion


# region polars protocol


@runtime_checkable
class PolarsDataFrameProtocol(Protocol):
    @property
    def columns(self) -> list[str]: ...

    def rows(self) -> list: ...


# endregion


@runtime_checkable
class DataSpecProvider(Protocol):
    def to_data_spec_source(self) -> Union[list[dict], dict]: ...
