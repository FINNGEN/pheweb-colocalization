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
```


Setup your development database

Load your database

SQLALCHEMY_DATABASE_URI

The standard sqlalchemy [database url](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls) are supported.


In addition the path of a mysql configuration file can be specified and is often used :

```
	export SQLALCHEMY_DATABASE_URI=./mysql.conf
```

Setting up a sqlite database is a convient to setup :


```
     export SQLALCHEMY_DATABASE_URI=sqlite:////tmp/tmp.db # setup environment
```

Create the database schema if it doesn't exist the database :


```
     flask colocalization init ${SQLALCHEMY_DATABASE_URI} # create schema
```

Load a colocalization file into your database :

```
     flask colocalization load ${SQLALCHEMY_DATABASE_URI} <datafile> # load data file into database
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

