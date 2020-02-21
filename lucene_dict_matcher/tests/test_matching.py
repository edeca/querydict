import pytest
from lucene_dict_matcher.parser import QueryEngine, MatchException

SIMPLE_DATA = {"key1": "value1", "key2": "value2"}
COMPLEX_DATA = {"country": "England", "data": {"weather": "Rainy"}}


def test_phrase():
    """ Ensure queries that generate a Phrase are matched """
    assert QueryEngine('key1:"value1"').match(SIMPLE_DATA)


def test_missing():
    """ Test for a key that does not exist, ensuring it does not raise an exception. """
    assert QueryEngine("key3:value3").match(SIMPLE_DATA) is False


def test_missing_nested():
    """ Test for a nested key that does not exist, ensuring it does not raise an exception. """
    assert QueryEngine("foo.bar.baz:missing").match(SIMPLE_DATA) is False


def test_simple_and():
    assert QueryEngine("key1:value1 AND key2:value2", short_circuit=True).match(SIMPLE_DATA) is True


def test_impossible_and():
    """ Test a condition that can never be true """
    assert QueryEngine("key1:value1 AND key1:value2", short_circuit=True).match(SIMPLE_DATA) is False
    assert QueryEngine("key1:value1 AND key1:value2", short_circuit=False).match(SIMPLE_DATA) is False


def test_simple_or():
    assert QueryEngine("key1:value1 OR key2:value2", short_circuit=True).match(SIMPLE_DATA)
    assert QueryEngine("key1:value1 OR key2:value2", short_circuit=False).match(SIMPLE_DATA)


def test_grouped_or():
    assert QueryEngine(
        "country:France OR (country:England AND data.weather:Rainy)"
    ).match(COMPLEX_DATA)


def test_nested():
    assert QueryEngine("country:England AND data.weather:Rainy").match(COMPLEX_DATA)


def test_ambiguous_and():
    """ Ensure the default action for ambiguous queries is AND """
    assert QueryEngine("key1:value1 key2:value2").match(SIMPLE_DATA)


def test_default_field():
    with pytest.raises(MatchException):
        QueryEngine("foo", allow_bare_field=True).match(SIMPLE_DATA)