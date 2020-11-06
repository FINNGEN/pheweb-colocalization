from finngen_common_data_model.genomics import Locus, Variant
from finngen_common_data_model.colocalization import Colocalization, CausalVariant
from pheweb_colocalization.model import CausalVariantVector, SearchSummary, SearchResults, PhenotypeList


def test_causal_variant_vector():
    causalVariantVector = CausalVariantVector(position = [],
                                              variant = [],
                                              pip1 = [],
                                              pip2 = [],
                                              beta1 = [],
                                              beta2 = [],
                                              causalvariantid = [],
                                              count_cs = [],
                                              phenotype1 = [],
                                              phenotype1_description = [],
                                              phenotype2 = [],
                                              phenotype2_description = [])
    expected =  {'beta1': [],
                 'beta2': [],
                 'causalvariantid': [],
                 'count_cs': [],
                 'phenotype1': [],
                 'phenotype1_description': [],
                 'phenotype2': [],
                 'phenotype2_description': [],
                 'pip1': [],
                 'pip2': [],
                 'position': [],
                 'variant': [] }
    actual = causalVariantVector.json_rep()
    assert expected == actual
    
def test_search_summary():
    searchSummary = SearchSummary(count = 1,
                                  unique_phenotype2 = 2,
                                  unique_tissue2 = 3)
    expected = { 'count' : 1,
                 'unique_phenotype2' : 2,
                 'unique_tissue2' : 3}
    actual = searchSummary.json_rep()
    assert expected == actual

def test_search_results():
    searchResults = SearchResults(count = 0,
                                  colocalizations = [])
    expected = { 'count' : 0 , 'colocalizations' : []}
    actual = searchResults.json_rep()
    assert expected == actual

def test_phenotype_list():
    phenotypeList = PhenotypeList(phenotypes = [])
    expecteed = { 'phenotypes' : [] }
    actual = phenotypeList.json_rep()
    assert expecteed == actual
