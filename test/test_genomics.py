import pytest

from finngen_common_data_model.genomics import Locus, Variant


def test_locus_bad_chromosome():
    with pytest.raises(ValueError):
        Locus(chromosome=30, start=2, stop=10)


def test_locus_from_str_1():
    expected = Locus(chromosome=15, start=78464464, stop=78864464)
    actual = Locus.from_str("15:78464464-78864464")
    assert expected == actual


def test_locus_from_str_2():
    expected = "15:78464464-78864464"
    actual = str(Locus.from_str("15:78464464-78864464"))
    assert expected == actual


def test_locus_parse_error():
    with pytest.raises(Exception):
        Locus.from_str("78864464")


def test_locus_bad_boundary():
    with pytest.raises(Exception):
        Locus.from_str("1:78864464:1")


def test_locus_json_rep():
    expected = {"chromosome": 15, "start": 78464464, "stop": 78864464}
    actual = Locus.from_str("15:78464464-78864464").json_rep()
    assert expected == actual


def test_locus_2():
    expected = "15:78464464-78864464"
    kwargs_rep = Locus.from_str("15:78464464-78864464").kwargs_rep()
    locus = Locus(**kwargs_rep)
    actual = str(locus)
    assert expected == actual


def test_variant_bad_chromosome():
    with pytest.raises(ValueError):
        Variant(chromosome=30, position=2, reference="A", alternate="G")


def test_variant_1():
    expected = Variant(chromosome=1, position=2, reference="A", alternate="G")
    actual = Variant.from_str("1_2_A_G")
    assert expected == actual


def test_variant_2():
    variant = "1_2_A_G"
    expected = "1:2:A:G"
    actual = str(Variant.from_str(variant))
    assert expected == actual


def test_variant_3():
    variant = "1_2_A_G"
    expected = "1:2:A:G"
    actual = str(Variant.from_str(variant))
    assert expected == actual


def test_variant_4():
    variant = "M_2_A_G"
    expected = "25:2:A:G"
    actual = str(Variant(**Variant.from_str(variant).kwargs_rep()))
    assert expected == actual


def test_variant_5():
    variant = "1:2:A:G"
    expected = "1:2:A:G"
    actual = str(Variant.from_str(variant))
    assert expected == actual


def test_variant_6():
    variant = "1_2_A/G"
    expected = "1:2:A:G"
    actual = str(Variant.from_str(variant))
    assert expected == actual


def test_variant_parse_error():
    with pytest.raises(Exception):
        Variant.from_str("78864464")


def test_structural_variants_1():
    expected = "9:96792507:T:<INS:ME:ALU>"
    variant = "chr9_96792507_T_<INS:ME:ALU>"
    actual = str(Variant.from_str(variant))
    assert expected == actual


def test_structural_variants_2():
    expected = "9:96792507:<INS:ME:ALU>:<INS:ME:ALU>"
    variant = "chr9_96792507_<INS:ME:ALU>_<INS:ME:ALU>"
    actual = str(Variant.from_str(variant))
    assert expected == actual


def test_order_key():
    acutal = map(Variant.from_str, ["1:2:A:G", "10:20:A:G", "3:4:C:A", "3:4:C:G", "1:2:A:A"])
    actual = sorted(list(acutal), key=Variant.sort_key)
    expected = list(map(Variant.from_str, ["1:2:A:A", "1:2:A:G", "3:4:C:A", "3:4:C:G", "10:20:A:G"]))
    assert expected == actual

def test_normalize_str():
    acutal = list(map(Variant.normalize_str, ["1:2-A-G", "10:20/A/G", "3:4:C:A", "3:4:C:G", "1:2:A:A"]))
    expected = ["1:2:A:G", "10:20:A:G", "3:4:C:A", "3:4:C:G", "1:2:A:A"]
    assert acutal == expected
