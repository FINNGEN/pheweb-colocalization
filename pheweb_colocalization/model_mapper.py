import typing
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, String, Float, Text, ForeignKey, Index
from sqlalchemy.orm import mapper, composite, relationship

from finngen_common_data_model.genomics import Variant, Locus
from finngen_common_data_model.colocalization import CausalVariant, Colocalization 

from pheweb_colocalization.model import CausalVariantVector, SearchSummary, SearchResults, PhenotypeList, ColocalizationDB

def refine_colocalization(c : Colocalization) -> Colocalization:
    c = {x: getattr(c, x) for x in Colocalization.column_names()}
    return Colocalization(**c)

def NullableVariant(chromosome : typing.Optional[str],
                    position : typing.Optional[int],
                    reference : typing.Optional[str],
                    alternate : typing.Optional[str]) -> typing.Optional[Variant] :
    if chromosome and position and reference and alternate:
        return Variant(chromosome, position, reference, alternate)
    else:
        return None

    
import attr
from attr.validators import instance_of
class C():
    #variant = attr.ib(validator=attr.validators.optional(instance_of(Variant)))
    
    pip1 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    beta1 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    
    pip2 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    beta2 = attr.ib(validator=attr.validators.optional(instance_of(float)))

    
    
class ColocalizationMapping():
    metadata = None
    colocalization_table = None
    
    @staticmethod
    def getMetadata():
        if not ColocalizationMapping.metadata:
            ColocalizationMapping.initialize()
        return ColocalizationMapping.metadata

    @staticmethod
    def getTables():
        if not ColocalizationMapping.metadata:
            ColocalizationMapping.initialize()
        return [ ColocalizationMapping.causal_variant_table,
                 ColocalizationMapping.colocalization_table ]

    @staticmethod
    def getIndices():
        if not ColocalizationMapping.metadata:
            ColocalizationMapping.initialize()
            return [ ColocalizationMapping.colocalization_chromosome ,
                     ColocalizationMapping.colocalization_start,
                     ColocalizationMapping.colocalization_stop,
                     ColocalizationMapping.colocalization_phenotype1,
                     ColocalizationMapping.colocalization_phenotype2,
                     ColocalizationMapping.causal_variant_chromosome_position,
            ]
        
    @staticmethod
    def initialize():
        metadata = MetaData()
        ColocalizationMapping.metadata = metadata

        # Table
        colocalization_table = Table('colocalization',
                                     metadata,
                                     *Colocalization.columns())

        ColocalizationMapping.colocalization_table = colocalization_table
        
        ColocalizationMapping.colocalization_chromosome = Index('colocalization_chromosome',
                                                                colocalization_table.c.chromosome)

        ColocalizationMapping.colocalization_start = Index('colocalization_start',
                                                           colocalization_table.c.start)

        ColocalizationMapping.colocalization_stop = Index('colocalization_stop',
                                                          colocalization_table.c.stop)

        ColocalizationMapping.colocalization_phenotype1 = Index('colocalization_phenotype1',
                                                                colocalization_table.c.phenotype1)
        
        ColocalizationMapping.colocalization_phenotype2 = Index('colocalization_phenotype2',
                                                                colocalization_table.c.phenotype2)

        causal_variant_table = Table('causal_variant',
                                     metadata,
                                     *CausalVariant.columns(),
                                     Column('colocalization_id', Integer, ForeignKey('colocalization.id')))

        ColocalizationMapping.causal_variant_table = causal_variant_table
        
        ColocalizationMapping.causal_variant_chromosome_position = Index('causal_variant_chromosome_position',
                                                                         causal_variant_table.c.variant_chromosome,
                                                                         causal_variant_table.c.variant_position)

        
        causal_variant_mapper = mapper(CausalVariant,
                                       causal_variant_table,
                                       properties = { 'variant': composite(NullableVariant,
                                                                           causal_variant_table.c.variant_chromosome,
                                                                           causal_variant_table.c.variant_position,
                                                                           causal_variant_table.c.variant_ref,
                                                                           causal_variant_table.c.variant_alt)
                                       })

        cluster_coordinate_mapper = mapper(Colocalization,
                                           colocalization_table,
                                           properties={'locus_id1': composite(Variant,
                                                                              colocalization_table.c.locus_id1_chromosome,
                                                                              colocalization_table.c.locus_id1_position,
                                                                              colocalization_table.c.locus_id1_ref,
                                                                              colocalization_table.c.locus_id1_alt),
                                                       'locus_id2': composite(Variant,
                                                                              colocalization_table.c.locus_id2_chromosome,
                                                                              colocalization_table.c.locus_id2_position,
                                                                              colocalization_table.c.locus_id2_ref,
                                                                              colocalization_table.c.locus_id2_alt),
                                                       
                                                       'locus': composite(Locus,
                                                                          colocalization_table.c.chromosome,
                                                                          colocalization_table.c.start,
                                                                          colocalization_table.c.stop),

                                                       'variants': relationship(CausalVariant),
                                       })
        
