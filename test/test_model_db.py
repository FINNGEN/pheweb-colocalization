from finngen_common_data_model.genomics import Locus, Variant
from finngen_common_data_model.colocalization import Colocalization, CausalVariant
from pheweb_colocalization.model_db import ColocalizationDAO, chunk
import uuid
import random

rel = random.randint(1, 10)

def count(n):
    for x in range(n):
        yield x

def test_chunk_1():
    actual = list(chunk(lambda : count(10),2))
    expected = [[0, 1],[2, 3],[4, 5],[6, 7],[8, 9]]
    assert actual == expected

def test_chunk_2():
    actual = list(chunk(lambda : count(11),2))
    expected = [[0, 1],[2, 3],[4, 5],[6, 7],[8, 9],[10]]
    assert actual == expected

def test_can_insert():
    dao = ColocalizationDAO('sqlite:///:memory:', echo = True)
    dao.create_schema()
    phenotype1 = "phenotype1"


    casual_variant1 = CausalVariant(rel = rel,
                                    causal_variant_id = 1,
                                    variant = Variant.from_str("chr1_2_A_C"),
                                    pip1 = 1.0,
                                    pip2 = 2.0,
                                    beta1 = 3.0,
                                    beta2 = 4.0)

    casual_variant2 = CausalVariant(rel = rel,
                                    causal_variant_id = 2,
                                    variant = Variant.from_str("chr1_10_G_T"),
                                    pip1 = 5.0,
                                    pip2 = 6.0,
                                    beta1 = 7.0,
                                    beta2 = 8.0)

    variants = [casual_variant1, casual_variant2]

    colocalization = Colocalization(rel = rel,
                                    colocalization_id=1,
                                    source1 = "source1",
                                    source2 = "source2",
                                    phenotype1 = phenotype1,
                                    phenotype1_description = "phenotype1_description",
                                    phenotype2 = "phenotype2",
                                    phenotype2_description = "phenotype2_description",
                                    tissue1 = "tissue1",
                                    tissue2 = "tissue2",

                                    locus_id1 = Variant.from_str("chr1_2_A_C"),
                                    locus_id2 = Variant.from_str("chr1_4_G_T"),

                                    locus = Locus(1, 8, 9),

                                    clpp = 10.0,
                                    clpa = 11.0,

                                    quant1 = None,
                                    quant2 = None,

                                    variants = variants,

                                    len_cs1 = 14,
                                    len_cs2 = 15,
                                    len_inter = 16,

                                    source2_displayname = "source2_displayname",

                                    beta1 = 0.1,
                                    beta2 = -0.1,
                                    pval1 = 0.001,
                                    pval2 = 0.005,
                                    
                                    )

    dao.save(colocalization)
    results = dao.get_variant(phenotype1, Variant.from_str("chr1_2_A_C"))
    assert results.count == 1
    assert results.colocalizations[0] == colocalization
    results = dao.get_locus(phenotype1, Locus.from_str("1:0-20"))
    assert results.count == 1
    results = dao.get_locus(phenotype1, Locus.from_str("1:100-200"))
    assert results.count == 0
