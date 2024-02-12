from collections import OrderedDict

import pytest
from typing import Dict, Any, Optional

from serde import from_dict, serde, SerdeError


@serde
class ErrorPrintingSubClass:
    int_value: int


@serde
class ErrorPrintingMainClass:
    sub: Optional[ErrorPrintingSubClass]
    int_value: int
    dict_value: Optional[Dict[str, Any]]


def test_error_printing_with_missing_key() -> None:
    data: Dict[str, Any] = {}
    with pytest.raises(SerdeError) as e:
        from_dict(ErrorPrintingMainClass, data)
    # Key error gets stripped and reduced to only the field
    assert "{}" in str(e.value)
    assert "KeyError: 'int_value'" in str(e.value)


def test_error_printing_with_dict_as_list() -> None:
    data = OrderedDict({"int_value": 1, "dict_value": [1, 2]})
    with pytest.raises(SerdeError) as e:
        from_dict(ErrorPrintingMainClass, data)
    assert "{'int_value': '1', 'dict_value': '[...]'}" in str(e.value)
    assert "AttributeError: 'list' object has no attribute 'items'" in str(e.value)


def test_error_printing_with_class_expecting_list_but_getting_single() -> None:
    data = {"int_value": 1, "sub": [{"int_value": 1}]}
    with pytest.raises(SerdeError) as e:
        from_dict(ErrorPrintingMainClass, data)
    assert "{'int_value': '1', 'sub': '[...]'}" in str(e.value)
    assert "AttributeError: 'list' object has no attribute 'items'" in str(e.value)
