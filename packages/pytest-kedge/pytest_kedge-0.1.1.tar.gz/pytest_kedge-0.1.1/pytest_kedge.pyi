from typing import Any, Callable, Dict, Generic, List, Type, TypeVar, Union

from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")

class TestCase(Generic[P]):
    name: str
    input: Dict[str, Any]
    expected: Union[Any, Type[Exception]]
    test_failure_message: str

    def __init__(
        self,
        name: str,
        input: Dict[str, Any],
        expected: Union[Any, Type[Exception]],
        test_failure_message: str,
    ) -> None: ...

class TestSuite(Generic[P, T]):
    target: Callable[P, T]
    scenarios: List[TestCase[P]]

    def __init__(
        self, target: Callable[P, T], scenarios: List[TestCase[P]]
    ) -> None: ...
