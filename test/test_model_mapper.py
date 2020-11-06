import pytest

from pheweb_colocalization.model_mapper import NullableVariant, ColocalizationMapping
 
def test_nullable_variant():
    assert None == NullableVariant(None,None,None,None)


def test_colocalization_mapping():
    with pytest.raises(Exception):
        assert None == ColocalizationMapping()

def test_get_tables():
    instance = ColocalizationMapping.getInstance()
    assert len(instance.getTables()) == 2
    assert len(instance.getIndices()) == 8
