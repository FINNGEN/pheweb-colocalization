import json
from flask import Blueprint, current_app as app, g, request
from finngen_common_data_model.genomics import Variant, Locus
import re

from pheweb_colocalization.model import CausalVariantVector, SearchSummary, SearchResults, PhenotypeList, ColocalizationDB

colocalization = Blueprint('colocalization', __name__)
development = Blueprint('development', __name__)


@colocalization.route('/api/colocalization', methods=["GET"])
def get_phenotype():
    app_dao = app.jeeves.colocalization
    if app_dao:
        flags = {}
        phenotypes = app_dao.get_phenotype(flags=flags)
    else:
        phenotypes = PhenotypeList([])
    return json.dumps(phenotypes.json_rep())

@colocalization.route('/api/colocalization/<string:phenotype>/<string:locus>', methods=["GET"])
def get_locus(phenotype: str,
              locus: str):
    app_dao = app.jeeves.colocalization
    if app_dao:
        flags = request.args.to_dict()
        result = app_dao.get_locus(phenotype=phenotype,
                                   locus = Locus.from_str(locus),
                                   flags=flags)
    else:
        result = SearchResults(colocalizations=[],
                               count=0)
    return json.dumps(result.json_rep(), default=lambda o: None)


@colocalization.route('/api/colocalization/<string:phenotype>/<string:locus>/summary', methods=["GET"])
def do_summary_colocalization(phenotype: str,
                              locus : str):
  app_dao = app.jeeves.colocalization
  if app_dao:
      flags = request.args.to_dict()
      summary = app_dao.get_locus_summary(phenotype=phenotype,
                                          locus = Locus.from_str(locus),
                                          flags=flags)
  else:
      summary = SearchSummary(count=0,
                              unique_phenotype2 = 0,
                              unique_tissue2 = 0)
  return json.dumps(summary.json_rep(), default=lambda o: None)


@colocalization.route('/api/colocalization/<string:phenotype>/lz-results/', methods=["GET"])
def get_locuszoom_results(phenotype: str):
    filter_param = request.args.get('filter')
    groups = re.match(r"analysis in 3 and chromosome in +'(.+?)' and position ge ([0-9]+) and position le ([0-9]+)", filter_param).groups()
    chromosome, start, stop = groups[0], int(groups[1]), int(groups[2])
    flags = request.args.to_dict()
    return get_locuszoom(phenotype, chromosome, start, stop, flags)

@colocalization.route('/api/colocalization/<string:phenotype>/<string:locus>/finemapping', methods=["GET"])
def get_locuszoom(phenotype: str,
                  locus : str,
                  flags = None):
    app_dao = app.jeeves.colocalization
    if app_dao:
        flags = flags or request.args.to_dict()
        locus = Locus.from_str(locus)
        variants = app_dao.get_locuszoom(phenotype=phenotype, locus = locus, flags=flags)
        variants = {k: v.json_rep() for k, v in variants.items()} if variants else []
    else:
        variants = {}
    return json.dumps(variants)

@development.route('/api/colocalization', methods=["POST"])
def post_phenotype1():
    f = request.files['csv']
    path = secure_filename(f.filename)
    path = os.path.join(upload_dir, path)
    f.save(path)
    return json.dumps(app_dao.load_data(path), default=lambda o: None)


@development.route('/api/colocalization/<int:colocalization_id>', methods=["GET"])
def get_colocalization(colocalization_id: int):
    app_dao = app.jeeves.colocalization
    flags = request.args.to_dict()
    results = app_dao.get_colocalization(colocalization_id)
    return json.dumps(results.json_rep() if results else None, default=lambda o: None)


