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

```
     export SQLALCHEMY_DATABASE_URI=sqlite:////tmp/tmp.db
     flask colocalization init ${SQLALCHEMY_DATABASE_URI}
     flask colocalization load ${SQLALCHEMY_DATABASE_URI} <datafile>
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
	
	
