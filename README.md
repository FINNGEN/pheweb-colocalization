# pheweb-colocalization
pheweb colocalization

# Quick start

Setup virtualenv

```
   python3 -m venv env
   source env/bin/activate
```

Install packages

```
   pip install .
```

Setup environment


```
   export FLASK_APP=`pwd`/pheweb_colocalization/app.py
   export PYTHON_PATH=`pwd`
   export RELEASE=10
```


## Setting up your development database



The standard sqlalchemy [database url](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls) are supported.
Set your uri :

```
export SQLALCHEMY_DATABASE_URI=
```


In addition the path of a mysql configuration file can be specified and is often used :

```
	export SQLALCHEMY_DATABASE_URI=/tmp/mysql.conf
```

mysql conf template:

```conf
mysql = {
     'host': '35.205.61.81',
     'db': 'analysis_r10',
     'user': 'pheweb_dev',
     'password': 'RETRACTED',
     'release': 10
}
```

Setting up a sqlite database is a convient to setup :


```
     export SQLALCHEMY_DATABASE_URI=sqlite:////tmp/tmp.db # setup environment
```

Create the database schema if it doesn't exist the database :


```
     flask colocalization init ${SQLALCHEMY_DATABASE_URI} # create schema
```

Load a colocalization file into your database (has to start with a slash) :

The order of columns of the file to be loaded are specified below.

> source1, source2, pheno1, pheno1\_description, pheno2, pheno2\_description, quant1, quant2, tissue1, tissue2, locus_id1, locus\_id2, chrom, start, stop, clpp, clpa, vars, len_cs1, len\_cs2, len_inter, vars1\_info, vars2\_info, source2\_displayname 

The following command may help rearrange columns.

```
cat $FILE | sqlite3 -csv ':memory:' '.headers on' '.separator "\t"' '.mode tabs' '.import /dev/stdin data' 'select source1, source2, pheno1, pheno1\_description, pheno2, pheno2\_description, quant1, quant2, tissue1, tissue2, locus_id1, locus\_id2, chrom, start, stop, clpp, clpa, vars, len_cs1, len\_cs2, len_inter, vars1\_info, vars2\_info, source2\_displayname from data' 
```

Alternatively, you can run workflow `wdl/format_colocs.wdl` in order to re-order columns, remove pvals from vars info, and add a source2_displayname column to the input colocalization files. Required inputs to the workflow are:
- `format_coloc.input_files` (Array[File]) - an array of colocalization files prepared by colocalization workflow. 
- `format_coloc.add_displayname` (Boolean) - specify whether to add `source2_displayname` column to each of the input colocalization files.
- `format_coloc.add_displayname_column.src2_displayname_map` (File) - tab-separated two-column, source2 and source2_displayname, CSV file used for preparing `source2_displayname` column.
- `format_coloc.reorder_columns` (Boolean) - specify whether to re-order columns (provide `format_coloc.reorder.cols_order` if the order is different from the default).
- `format_coloc.reorder.cols_order` (String) - tab-separated two-column, source2 and source2_displayname, CSV file used for preparing source2_displayname column, default columns string: "source1,source2,pheno1,pheno1_description,pheno2,pheno2_description,quant1,quant2,tissue1,tissue2,locus_id1,locus_id2,chrom,start,stop,clpp,clpa,vars,len_cs1,len_cs2,len_inter,vars1_info,vars2_info,source2_displayname".
- `format_coloc.remove_pvals_from_vars_info_column` (Boolean) - specify whether to remove p-values from from vars_info column.

Sample CSV file used as input in `format_coloc.add_displayname_column.src2_displayname_map`:
```
source2 source2_displayname
FinnGen FinnGen
geneRISK        geneRISK
INTERVAL        INTERVAL
UKBB    UKBB
Olink   FinnGen Olink batch 1,2
SomaScan        FinnGen Somascan batch 1,2
Alasoo_2018     Alasoo_2018 (eQTL Catalog, RNA-seq data)
BLUEPRINT       BLUEPRINT (eQTL Catalog, RNA-seq data)
BrainSeq        BrainSeq (eQTL Catalog, RNA-seq data)
CEDAR   CEDAR (eQTL Catalog, Microarray data)
Fairfax_2012    Fairfax_2012 (eQTL Catalog, Microarray data)
Fairfax_2014    Fairfax_2014 (eQTL Catalog, Microarray data)
GENCORD GENCORD (eQTL Catalog, RNA-seq data)
...
```

The outputs of the workflow can be used for the loading to the db using the command below.


```
     flask colocalization load ${RELEASE} ${SQLALCHEMY_DATABASE_URI} <datafile> # load data file into database
```

If you wish to delete the colocalization data from the database :

```
     flask colocalization delete ${SQLALCHEMY_DATABASE_URI} # delete schema
```


Additional commands

```
	 flask colocalization --help # command help
	 flask colocalization schema ${SQLALCHEMY_DATABASE_URI} # output schema
```


The endpoints

```
     # Get the list of phenotypes
     curl http://127.0.0.1:5000/api/colocalization
     # examples
     # export PHENOTYPE=AB1_ARTHROPOD
     # export LOCUS=1_115975000_115977000
     # export COLOCALIZATION_ID=1
     # colocalization results for locus
     curl http://127.0.0.1:5000/api/colocalization/$PHENOTYPE/$LOCUS
     # summary of colocalization results for locus
     curl http://127.0.0.1:5000/api/colocalization/$PHENOTYPE/$LOCUS/summary
     # this end point use used for lozus zoom
     curl http://127.0.0.1:5000/api/colocalization/$PHENOTYPE/$LOCUS/finemapping
     # get specific colocolization record 
     curl http://127.0.0.1:5000/api/colocalization/$COLOCALIZATION_ID
```

# Development
	
	
Install packages

```
   pip install .[dev]
```

