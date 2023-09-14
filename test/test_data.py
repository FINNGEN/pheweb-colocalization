from finngen_common_data_model.data import *


def test_na():
    assert (na(str))("") == ""
    assert (na(str))("na") is None
    assert (na(str))("NA") is None


def test_ascii():
    assert only_ascii("") == ""
    assert only_ascii("na") == "na"
    assert only_ascii("AlzheimerÕs disease") == "Alzheimers disease"


def test_nvl():
    assert nvl(None, id) is None
    assert nvl("", int) is None
    assert nvl("1", int) == 1
