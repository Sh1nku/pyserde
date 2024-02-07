import pytest

from serde import from_dict, serde, SerdeError


def test_error_printing_with_missing_key() -> None:
    @serde
    class TestClass:
        a: int
        b: int

    data = {"b": 1, "c": {"d": {}}, "e": ["1", "2"]}
    with pytest.raises(SerdeError) as e:
        from_dict(TestClass, data)
        assert (
            str(e)
            == "While deserializing TestClass, "
            + "did not find key 'a' in {'b': '1', 'c': '...', 'e': '...'}"
        )
