# hillel_05_2022_support

[![Builds Status](https://github.com/SergKirichenko/hillel_05_2022_support/actions/workflows/Test-code.yml/badge.svg?)](https://github.com/SergKirichenko/hillel_05_2022support/actions/workflows/Test-code.yml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/SergKirichenko/hillel_05_2022_support/blob/main/.pre-commit-config.yaml)
___

# Project: Support service

Online support service for users. Helps to organize quick and comfortable connection 
specialists of service with users issues.
___
## Setup Environment
#### 1)  Install pipenv
- About [pipenv](https://pypi.org/project/pipenv/)

```
$ pip instal pipenv
$ pipenv shell   # activate vitual environment
```
#### 2) Installing dependencies
'''All of dependencies wrote in Pipfile'''
```
$ pipenv install   # installs all packages from Pipfile.
``` 
___
## Description 
#### Authentication
- Have the panel of administration  with database of users. Can sign up, sign in/out. 
Also in app can assign to role of user. 
  - migrations/ - Has a files with descriptions all fields of database model of admin panel
  - admin.py - the admin panel itself
  - models.py - the model for working with database 
  

#### Core
- Tickets - can work with tickets of users requests. App have a database of a tickets.
- Comments  - can work with comments of users. App have a database of comments to the tickets.
- Exchange Rate - app can doing request for updating of currency rate and make to respose in json format. 
App can save information in history file and make output respose in json format from request.

#### Shared
- A special utility makes temporary marks when adding or changing data in the database 

#### Others files
- __history.json__ - Keep in history of exchange rate. 
- __manage.py__ - script for managing our project, created by the django-admin command. used to build applications, work with databases, and to run or debug-run the server.
- *.flake8* - Flake8 config file
- *pyproject.toml* - config file for Black and Isort 
- *Pipfile* - is the dedicated file used by the Pipenv virtual environment to manage project dependencies
- *Pipfile.lock* - is intended to specify, based on the packages present in Pipfile, which specific version of those should be used, avoiding the risks of automatically upgrading packages that depend upon each other and breaking our project dependency tree
- .pre-commit-config.yaml - config file of pre-commit hooks for checking code quality