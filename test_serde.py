import json
import msgpack
from dataclasses import dataclass

from serde import serialize, deserialize
from serde.json import to_json, from_json
from serde.msgpack import to_msgpack, from_msgpack


def test_json_se_primitive():
    @serialize
    @dataclass
    class Hoge:
        i: int
        s: str
        f: float
        b: bool

    h = Hoge(i=10, s='hoge', f=100.0, b=True)
    assert '{"i": 10, "s": "hoge", "f": 100.0, "b": true}' == to_json(h)


def test_json_de_primitive():
    @deserialize
    @dataclass
    class Hoge:
        i: int
        s: str
        f: float
        b: bool

    h = Hoge(i=10, s='hoge', f=100.0, b=True)
    assert h == from_json(Hoge, """
                                {"i": 10,
                                 "s": "hoge",
                                 "f": 100.0,
                                 "b": true}""")


def test_json_se_nested():
    @deserialize
    @dataclass
    class Foo:
        i: int
        s: str
        f: float
        b: bool

    @serialize
    @dataclass
    class Hoge:
        i: int
        s: str
        f: float
        b: bool
        foo: Foo

    f = Foo(i=20, s='foo', f=200.0, b=False)
    h = Hoge(i=10, s='hoge', f=100.0, b=True, foo=f)
    expected = """
               {"i": 10,
                "s": "hoge",
                "f": 100.0,
                "b": true,
                "foo" : {
                    "i": 20,
                    "s": "foo",
                    "f": 200.0,
                    "b": false}}
               """
    assert json.loads(expected) == json.loads(to_json(h))


def test_json_de_nested():
    @deserialize
    @dataclass
    class Foo:
        i: int
        s: str
        f: float
        b: bool

    @deserialize
    @dataclass
    class Hoge:
        i: int
        s: str
        f: float
        b: bool
        foo: Foo

    f = Foo(i=20, s='foo', f=200.0, b=False)
    h = Hoge(i=10, s='hoge', f=100.0, b=True, foo=f)
    hh = from_json(Hoge, """
                         {"i": 10,
                          "s": "hoge",
                          "f": 100.0,
                          "b": true,
                          "foo" : {
                              "i": 20,
                              "s": "foo",
                              "f": 200.0,
                              "b": false}}
                         """)
    assert h == hh


def test_msgpack_se_primitive():
    @serialize
    @dataclass
    class Hoge:
        i: int
        s: str
        f: float
        b: bool

    h = Hoge(i=10, s='hoge', f=100.0, b=True)
    expected = msgpack.packb((10, 'hoge', 100.0, True))
    assert expected == to_msgpack(h)


def test_msgpack_de_primitive():
    @deserialize
    @dataclass
    class Hoge:
        i: int
        s: str
        f: float
        b: bool

    h = Hoge(i=10, s='hoge', f=100.0, b=True)
    packed = msgpack.packb((10, 'hoge', 100.0, True))
    assert h == from_msgpack(Hoge, packed)
