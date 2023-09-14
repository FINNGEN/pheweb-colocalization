from finngen_common_data_model.genomics import Locus, Variant
import attr
import uuid
from finngen_common_data_model.colocalization import Colocalization as BaseColocalization, \
    CausalVariant as BaseCausalVariant
from finngen_common_data_model.genomics import Locus, Variant

rel = 123

@attr.s(frozen=True, slots=True)
class Colocalization(BaseColocalization):
    None


@attr.s(frozen=True, slots=True)
class CausalVariant(BaseCausalVariant):
    None


def test_parse_causal_variant():
    actual = CausalVariant.parse_causal_variant('1_1_A_A,0.02,0.19')
    expected = (0.02, 0.19)
    assert expected == actual


causal_variants = [CausalVariant(1,0.1, 0.11, 0.2, 0.22, None, Variant.from_str("1_1_A_G")),
                   CausalVariant(2,0.1, 0.11, None, None, None, Variant.from_str("1_1_A_G")),
                   CausalVariant(3,None, None, 0.2, 0.22, None, Variant.from_str("1_1_A_G")),
                   CausalVariant(4,None, None, None, None, None, Variant.from_str("1_1_A_G"))]


def test_has_cs1():
    actual = list(map(lambda c: c.has_cs1(), causal_variants))
    expected = [True, True, False, False]
    assert expected == actual


def test_has_cs2():
    actual = list(map(lambda c: c.has_cs2(), causal_variants))
    expected = [True, False, True, False]
    assert expected == actual


def test_count_cs1():
    actual = list(map(lambda c: c.count_cs1(), causal_variants))
    expected = [1, 1, 0, 0]
    assert expected == actual


def test_count_cs2():
    actual = list(map(lambda c: c.count_cs2(), causal_variants))
    expected = [1, 0, 1, 0]
    assert expected == actual


def test_count_cs():
    actual = list(map(lambda c: c.count_cs(), causal_variants))
    expected = [2, 1, 1, 0]
    assert expected == actual


def test_membership_cs():
    actual = list(map(lambda c: c.membership_cs(), causal_variants))
    expected = ['Both', 'CS1', 'CS2', 'None']
    assert expected == actual


def test_causal_variants_kwargs_rep():
    actual = list(map(lambda c: c.kwargs_rep(), causal_variants))
    expected = [{ 'rel': 1, 'beta1': 0.11, 'beta2': 0.22, 'pip1': 0.1, 'pip2': 0.2,
                 'variant': Variant(chromosome=1, position=1, reference='A', alternate='G'), 'causal_variant_id': None},
                { 'rel': 2, 'beta1': 0.11, 'beta2': None, 'pip1': 0.1, 'pip2': None,
                 'variant': Variant(chromosome=1, position=1, reference='A', alternate='G'), 'causal_variant_id': None},
                { 'rel': 3, 'beta1': None, 'beta2': 0.22, 'pip1': None, 'pip2': 0.2,
                 'variant': Variant(chromosome=1, position=1, reference='A', alternate='G'), 'causal_variant_id': None},
                { 'rel': 4, 'beta1': None, 'beta2': None, 'pip1': None, 'pip2': None,
                 'variant': Variant(chromosome=1, position=1, reference='A', alternate='G'), 'causal_variant_id': None}]
    assert expected == actual


def test_json_rep():
    actual = list(map(lambda c: c.json_rep(), causal_variants))
    expected = [
        { 'rel': 1, 'beta1': 0.11, 'beta2': 0.22, 'count_cs': 2, 'membership_cs': 'Both', 'pip1': 0.1, 'pip2': 0.2, 'position': 1,
         'variant': '1:1:A:G', 'causal_variant_id': None},
        { 'rel': 2, 'beta1': 0.11, 'beta2': None, 'count_cs': 1, 'membership_cs': 'CS1', 'pip1': 0.1, 'pip2': None, 'position': 1,
         'variant': '1:1:A:G', 'causal_variant_id': None},
        { 'rel': 3, 'beta1': None, 'beta2': 0.22, 'count_cs': 1, 'membership_cs': 'CS2', 'pip1': None, 'pip2': 0.2, 'position': 1,
         'variant': '1:1:A:G', 'causal_variant_id': None},
        { 'rel': 4, 'beta1': None, 'beta2': None, 'count_cs': 0, 'membership_cs': 'None', 'pip1': None, 'pip2': None,
         'position': 1, 'variant': '1:1:A:G', 'causal_variant_id': None}]
    assert expected == actual


def test_causal_variant_from_list_1():
    vars1_info = "1_1_A_A,0.02,0.19;1_1_A_G,0.01,0.12;1_1_C_A,0.03,0.18;1_1_C_T,0.05,0.15;1_1_G_G,0.02,0.19;1_1_G_T,0.04,0.49;1_1_T_C,0.04,0.19;1_1_T_G,0.03,0.17"
    vars2_info = "1_1_G_A,0.01,0.19;1_1_T_C,0.02,0.12;1_1_C_G,0.65,0.19"
    expected = {
        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='A',
                                      alternate='A'),
                      pip1=0.02,
                      beta1=0.19,
                      pip2=None,
                      beta2=None),

        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='A',
                                      alternate='G'),
                      pip1=0.01,
                      beta1=0.12,
                      pip2=None,
                      beta2=None),

        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='C',
                                      alternate='A'),
                      pip1=0.03,
                      beta1=0.18,
                      pip2=None,
                      beta2=None),

        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='C',
                                      alternate='G'),
                      pip1=None,
                      beta1=None,
                      pip2=0.65,
                      beta2=0.19),

        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='C',
                                      alternate='T'),
                      pip1=0.05,
                      beta1=0.15,
                      pip2=None,
                      beta2=None),

        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='G',
                                      alternate='A'),
                      pip1=None,
                      beta1=None,
                      pip2=0.01,
                      beta2=0.19),

        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='G',
                                      alternate='G'),
                      pip1=0.02,
                      beta1=0.19,
                      pip2=None,
                      beta2=None),

        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='G',
                                      alternate='T'),
                      pip1=0.04,
                      beta1=0.49,
                      pip2=None,
                      beta2=None),

        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='T',
                                      alternate='C'),
                      pip1=0.04,
                      beta1=0.19,
                      pip2=0.02,
                      beta2=0.12),

        CausalVariant(rel=rel,
                      variant=Variant(chromosome=1,
                                      position=1,
                                      reference='T',
                                      alternate='G'),
                      pip1=0.03,
                      beta1=0.17,
                      pip2=None,
                      beta2=None),
    }
    actual = CausalVariant.from_list(rel,vars1_info, vars2_info)
    actual = set(map(lambda c: CausalVariant(**c.kwargs_rep()), actual))
    assert expected == actual


def test_colocalization_kwargs_rep():
    variants = [BaseCausalVariant(rel=rel,
                                  variant=Variant(chromosome=1,
                                                  position=1,
                                                  reference='G',
                                                  alternate='A'),
                                  pip1=None,
                                  beta1=None,
                                  pip2=0.01,
                                  beta2=0.19,
                                  causal_variant_id=None),
                BaseCausalVariant(rel=rel,
                                  variant=Variant(chromosome=1,
                                                  position=1,
                                                  reference='A',
                                                  alternate='A'),
                                  pip1=0.02,
                                  beta1=0.19,
                                  pip2=None,
                                  beta2=None,
                                  causal_variant_id=None)]

    expected = {'rel' : rel,
                'colocalization_id': 5,
                'clpa': 11.0,
                'clpp': 10.0,
                'len_cs1': 1,
                'len_cs2': 2,
                'len_inter': 3,
                'locus': Locus(chromosome=7, start=8, stop=9),
                'locus_id1': Variant(chromosome=1, position=2, reference='C', alternate='A'),
                'locus_id2': Variant(chromosome=3, position=4, reference='C', alternate='A'),
                'phenotype1': 'phenotype1',
                'phenotype1_description': 'phenotype1_description',
                'phenotype2': 'phenotype2',
                'phenotype2_description': 'phenotype2_description',
                'quant1': None,
                'quant2': None,
                'source1': 'source1',
                'source2': 'source2',
                'tissue1': 'tissue1',
                'tissue2': 'tissue2',
                'variants': variants,
                'source2_displayname': 'source2_displayname', }

    colocalization = Colocalization(rel=rel,

                                    colocalization_id=5,

                                    source1='source1',
                                    source2='source2',

                                    phenotype1='phenotype1',
                                    phenotype1_description='phenotype1_description',

                                    phenotype2='phenotype2',
                                    phenotype2_description='phenotype2_description',

                                    quant1=None,
                                    quant2=None,

                                    tissue1='tissue1',
                                    tissue2='tissue2',

                                    locus_id1=Variant(chromosome=1,
                                                      position=2,
                                                      reference='C',
                                                      alternate='A'),
                                    locus_id2=Variant(chromosome=3,
                                                      position=4,
                                                      reference='C',
                                                      alternate='A'),

                                    locus=Locus(chromosome=7,
                                                start=8,
                                                stop=9),

                                    clpp=10.0,
                                    clpa=11.0,

                                    len_cs1=1,
                                    len_cs2=2,

                                    len_inter=3,
                                    variants=variants,

                                    source2_displayname='source2_displayname',)
    assert colocalization.kwargs_rep()['variants'] == variants
    assert colocalization.kwargs_rep() == expected


def test_colocalization_1():
    sample = ["source1",  # 0 source1
              "source2",  # 1 source2

              "phenotype1",  # 2 phenotype1
              "phenotype1_description",  # 3 phenotype1_description

              "phenotype2",  # 4 phenotype2
              "phenotype2_description",  # 5 phenotype2_description

              "",  # 6 quant1
              "",  # 7 quant2

              "tissue1",  # 8 tissue1
              "tissue2",  # 9 tissue2

              "1_2_C_A",  # 10 locus_id1
              "3_4_C_A",  # 11 locus_id2

              7,  # 12 chromosome
              8,  # 13 start
              9,  # 14 stop

              10.0,  # 15 clpp
              11.0,  # 16 clpa

              None,  # 17 var

              1,  # 18 len_cs1
              2,  # 19 len_cs2
              3,  # 20 len_inter

              # 21 variant 1
              "1_1_A_A,0.02,0.19",
              # 22 variant 2
              "1_1_G_A,0.01,0.19",
              "source2_displayname",
              ]

    expected = BaseColocalization(rel=rel,

                                  source1='source1',
                                  source2='source2',

                                  phenotype1='phenotype1',
                                  phenotype1_description='phenotype1_description',

                                  phenotype2='phenotype2',
                                  phenotype2_description='phenotype2_description',

                                  quant1=None,
                                  quant2=None,

                                  tissue1='tissue1',
                                  tissue2='tissue2',

                                  locus_id1=Variant(chromosome=1,
                                                    position=2,
                                                    reference='C',
                                                    alternate='A'),
                                  locus_id2=Variant(chromosome=3,
                                                    position=4,
                                                    reference='C',
                                                    alternate='A'),

                                  locus=Locus(chromosome=7,
                                              start=8,
                                              stop=9),

                                  clpp=10.0,
                                  clpa=11.0,

                                  len_cs1=1,
                                  len_cs2=2,

                                  len_inter=3,
                                  variants=[BaseCausalVariant(rel=rel,
                                                              variant=Variant(chromosome=1,
                                                                              position=1,
                                                                              reference='A',
                                                                              alternate='A'),
                                                              pip1=0.02,
                                                              beta1=0.19,
                                                              pip2=None,
                                                              beta2=None),
                                            BaseCausalVariant(rel=rel,
                                                              variant=Variant(chromosome=1,
                                                                              position=1,
                                                                              reference='G',
                                                                              alternate='A'),
                                                              pip1=None,
                                                              beta1=None,
                                                              pip2=0.01,
                                                              beta2=0.19),
                                            ],
                                  source2_displayname = "source2_displayname",
                                  )

    sample = "\t".join(map(str, sample))
    actual = Colocalization.from_str(rel,sample)
    assert expected == actual

# def test_colocalization_2():
#     sample = ['finemapping',
#               'AXV',
#               'AB1',
#               'ART',
#               'ENSG00000163393.13_1_115976513_115976613',
#               'SLC22A15.13_1_115976513_115976613',
#               '',
#               'exon',
#               '',
#               'brain_naive',
#               '1_11_C_A',
#               '1_11_A_G',
#               '1',
#               '115867263',
#               '116115414',
#               '0.0184555053710938',
#               '0.357658386230469',
#               '1_11_A_G,1_11_G_A,1_11_A_G',
#               '56',
#               '19',
#               '17',
#               '1_11_C_A,0.03,0.18;1_11_A_G,0.15,0.21']


#     expected = {}
#     sample = "\t".join(map(str,sample))
#     actual = Colocalization.from_str(sample)
#     assert expected == actual
