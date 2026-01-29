from typing import Union
from ._protocols import PandasDataFrameProtocol, PolarsDataFrameProtocol


TDataSpecSource = Union[
    list[dict], dict, PandasDataFrameProtocol, PolarsDataFrameProtocol
]
