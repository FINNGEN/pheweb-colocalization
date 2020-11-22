import typing
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, String, Float, Text, ForeignKey, Index
from sqlalchemy.orm import sessionmaker

from finngen_common_data_model.genomics import Variant, Locus
from finngen_common_data_model.colocalization import CausalVariant, Colocalization 

from pheweb_colocalization.model import CausalVariantVector, SearchSummary, SearchResults, PhenotypeList, ColocalizationDB
from pheweb_colocalization.model_mapper import ColocalizationMapping

import csv
import gzip
import attr
from .dao_support import DAOSupport
from sqlalchemy import func, distinct, or_, and_
import os
import sys
import importlib.machinery
import importlib.util
from sqlalchemy.sql import func

def refine_colocalization(c : Colocalization):
    return Colocalization(**c.kwargs_rep())


def chunk(iterable, size):
    buffer = []
    for v in iterable():
        buffer.append(v)
        if(len(buffer) >= size):
            yield buffer
            buffer = []
    if buffer:
        yield buffer
# TODO remove
csv.field_size_limit(sys.maxsize)

class ColocalizationDAO(ColocalizationDB):
    # Large credible sets result in
    # long running queries and huge
    # result sets ~90M.  Using this
    # threshold the results sets are
    # made smaller.
    CREDIBLE_SET_LENGTH_THRESHOLD = 1000
    
    @staticmethod
    def mysql_config(path : str) -> typing.Optional[str] :
        print(path)
        if os.path.exists(path):
            loader = importlib.machinery.SourceFileLoader('auth_module',path)
            spec = importlib.util.spec_from_loader(loader.name, loader)
            auth_module = importlib.util.module_from_spec(spec)
            loader.exec_module(auth_module)

            user = getattr(auth_module, 'mysql')['user']
            password = getattr(auth_module, 'mysql')['password']
            host = getattr(auth_module, 'mysql')['host']
            db = getattr(auth_module, 'mysql')['db']
            return 'mysql://{}:{}@{}/{}'.format(user,password,host,db)
        else:
            return path

    def __init__(self, db_url: str, echo=False, parameters=dict()):

        self.db_url=ColocalizationDAO.mysql_config(db_url)
        print("ColocalizationDAO : {}".format(self.db_url))
        self.engine = create_engine(self.db_url,
                                    pool_pre_ping=True,
                                    echo=echo,
                                    *parameters)
        self.mapping = ColocalizationMapping.getInstance()
        self.mapping.getMetadata().bind = self.engine
        self.Session = sessionmaker(bind=self.engine)
        self.support = DAOSupport(Colocalization)


    def __del__(self):
        if hasattr(self, 'engine') and self.engine:
            self.engine.dispose()

    def create_schema(self):
        return self.mapping.getMetadata().create_all(self.engine)

    def dump(self):
        print(self.db_url)
        # see  : https://stackoverflow.com/questions/2128717/sqlalchemy-printing-raw-sql-from-create
        def metadata_dump(sql, *multiparams, **params):
            print(sql.compile(dialect=engine.dialect))
        engine = create_engine(self.db_url, strategy='mock', executor=metadata_dump)
        self.mapping.getMetadata().create_all(engine)

    def delete_all(self):
        for table in self.mapping.getTables():
            self.engine.execute(table.delete())
        self.mapping.getMetadata().drop_all(self.engine)

    
    def load_data(self, release: int, path: str, header : bool=True) -> typing.Tuple[typing.Optional[int],typing.Optional[int]]:
        count = 0
        session = self.Session()
        colocalization_id = 1 + (session.query(func.max(Colocalization.colocalization_id)).scalar() or 0)
        causal_variant_id = 1 + (session.query(func.max(CausalVariant.causal_variant_id)).scalar() or 0)
        session.close()
        session = self.Session()        
        for index in self.mapping.getIndices():
             index.drop()
        try:
            def generate_colocalization(colocalization_id, causal_variant_id):
                with gzip.open(path, "rt") if path.endswith("gz") else open(path, 'r') as csv_file:
                    reader = csv.reader(csv_file, delimiter='\t', )
                    
                    if header:
                        actual_header = next(reader)
                        assert Colocalization.cvs_column_names() == actual_header, \
                            "header expected '{expected_header}' got '{actual_header}'".format(expected_header=expected_header,
                                                                                               actual_header=actual_header)

                    for line in reader:
                        try:
                            dto = Colocalization.from_list(release,line)
                            dto.colocalization_id = colocalization_id
                            colocalization_id = colocalization_id + 1
                            for v in dto.variants:
                                v.causal_variant_id = causal_variant_id
                                causal_variant_id = causal_variant_id + 1

                            yield dto
                        except Exception as e:
                            print(line)
                            print(e)
                            print("file:{}".format(path), file=sys.stderr, flush=True)
                            print(line, file=sys.stderr, flush=True)
                            raise

            for dtos in chunk(lambda : generate_colocalization(colocalization_id, causal_variant_id),100):
                dtos = list(dtos)
                print('.', flush=True, end='')
                session.add_all(dtos)
                count += len(dtos)
                session.flush()
                del dtos
            session.commit()
        finally:
            print()
            for index in self.mapping.getIndices():
                index.create()
        return count

    def save(self,colocalization : Colocalization) -> None:
        session = self.Session()
        session.add(colocalization)
        session.commit()


    def get_phenotype(self,
                      flags: typing.Dict[str, typing.Any]={}) -> typing.List[str]:
        session = self.Session()
        q = session.query(distinct(Colocalization.phenotype1))
        matches = self.support.create_filter(q, flags)
        return PhenotypeList(phenotypes = [r[0] for r in q.all()])
        return phenotype1

    def locus_query(self,
                    phenotype: str,
                    locus: Locus,
                    flags: typing.Dict[str, typing.Any]={},
                    projection = [Colocalization]):
        locus_id = Colocalization.variants.any(and_(CausalVariant.variant_chromosome == locus.chromosome,
                                                    CausalVariant.variant_position >= locus.start,
                                                    CausalVariant.variant_position <= locus.stop))
        
        colocalization_filter = and_(Colocalization.phenotype1 == phenotype,
                                     Colocalization.chromosome == locus.chromosome,
                                     Colocalization.len_cs2 < ColocalizationDAO.CREDIBLE_SET_LENGTH_THRESHOLD)
        phenotype1 = Colocalization.phenotype1 == phenotype
        session = self.Session()
        return [session, session
                         .query(*projection)
                         .select_from(Colocalization)
                         .filter(or_(locus_id))
                         .filter(colocalization_filter) ]

    
    def get_locus(self,
                  phenotype: str,
                  locus: Locus,
                  flags: typing.Dict[str, typing.Any]={}) -> SearchResults:
        """
        Search for colocalization that match
        the locus and range and return them.

        :param phenotype: phenotype to match in search
        :param chromosome_range: chromosome range to search
        :param flags: a collection   of optional flags

        :return: matching colocalizations
        """
        [session,query] = self.locus_query(phenotype, locus, flags)
        matches = query.all()
        matches = [ refine_colocalization(x) for x in matches]
        return SearchResults(colocalizations=matches,
                             count=len(matches))

    def get_locuszoom(self,
                        phenotype: str,
                        locus: Locus,
                        flags: typing.Dict[str, typing.Any]={}) -> typing.Dict[str, CausalVariantVector]   :
        """
        Search for colocalization that match
        the locus and range and return them.

        :param phenotype: phenotype to match in search
        :param chromosome_range: chromosome range to search
        :param flags: a collection of optional flags

        :return: matching colocalizations
        """
        [session,query] = self.locus_query(phenotype, locus, flags)
        session.expire_all()
        rows = {}
        for r in query.all():
            variants = map(lambda r : r.json_rep(), r.variants)
            variants = map(lambda v: [v["position"],
                                      v["variant"],
                                      v["pip1"],
                                      v["pip2"],
                                      v["beta1"],
                                      v["beta2"],
                                      v["causal_variant_id"],
                                      v["count_cs"],
                                      r.phenotype1,
                                      r.phenotype1_description,
                                      r.phenotype2,
                                      r.phenotype2_description
                                    ], variants)
            variants = list(map(list,zip(*variants)))
            if variants:
                position = variants[0]
                variant = variants[1]
                pip1 = variants[2]
                pip2 = variants[3]
                beta1 = variants[4]
                beta2 = variants[5]
                causal_variant_id = variants[6]
                count_cs = variants[7]
                phenotype1 = variants[8]
                phenotype1_description = variants[9]
                phenotype2 = variants[10]
                phenotype2_description = variants[11]
            else:
                position = []
                variant = []
                pip1 = []
                pip2 = []
                beta1 = []
                beta2 = []
                causal_variant_id = []
                count_cs = []
                phenotype1 = []
                phenotype1_description = []
                phenotype2 = []
                phenotype2_description = []
                
            rows[r.colocalization_id] = CausalVariantVector(position,
                                                            variant,
                                                            pip1,
                                                            pip2,
                                                            beta1,
                                                            beta2,
                                                            causal_variant_id,
                                                            count_cs,
                                                            phenotype1,
                                                            phenotype1_description,
                                                            phenotype2,
                                                            phenotype2_description)




        return rows
    
    def get_locus_summary(self,
                          phenotype: str,
                          locus: Locus,
                          flags: typing.Dict[str, typing.Any] = {}) -> SearchSummary:
        aggregates =  [func.count('*'),
                       func.count(distinct('colocalization.phenotype2')),
                       func.count(distinct('colocalization.tissue2'))]
        [session,query] = self.locus_query(phenotype, locus, flags, aggregates)
        session.expire_all()
        count, unique_phenotype2, unique_tissue2 = query.all()[0]
        return SearchSummary(count=count,
                             unique_phenotype2 = unique_phenotype2,
                             unique_tissue2 = unique_tissue2)

    def get_variant(self,
                    phenotype: str,
                    variant: Variant,
                    flags: typing.Dict[str, typing.Any] = {}) -> SearchResults:
        session = self.Session()
        matches = self.support.query_matches(session,
                                             flags={**{"phenotype1": phenotype,
                                                       "locus_id1_chromosome": variant.chromosome,
                                                       "locus_id1_position": variant.position,
                                                       "locus_id1_reference": variant.reference,
                                                       "locus_id1_alternate": variant.alternate,
                                             },**flags},
                                             f=refine_colocalization)
        session.expire_all()
        return SearchResults(colocalizations=matches,
                             count=len(matches))
        
    def get_colocalization(self,
                           colocalization_id : int,
                           flags: typing.Dict[str, typing.Any] = dict()) -> typing.Optional[Colocalization]:
        session = self.Session()
        matches = session.query(Colocalization).filter(Colocalization.id == colocalization_id).one_or_none()
        return matches

