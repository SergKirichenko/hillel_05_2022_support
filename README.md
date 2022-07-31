# hillel_05_2022_support


[![Builds Status](https://github.com/SergKirichenko/hillel_05_2022_support/actions/workflows/Test-code.yml/badge.svg?)](https://github.com/SergKirichenko/hillel_05_2022support/actions/workflows/Test-code.yml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/SergKirichenko/hillel_05_2022_support/blob/main/.pre-commit-config.yaml)

# Project: Support service

Online support service for users. Helps to organize quick and comfortable connection 
specialists of service with users issues.

## Setup the Environment
#### Install pipenv

```
$pip instal pipenv
```

## Description 
#### Authentication
- Have the panel of administration  with database of users. Can sign up, sign in/out. 
Also in app can assign to role of user. 

#### Core
- Tickets - can work with tickets of users requests. App have a database of a tickets.
- Comments  - can work with comments of users. App have a database of comments to the tickets.
- Exchange Rate - app can doing request for updating of currency rate and make to respose in json format. 
App can save information in history file and make output respose in json format from request.
