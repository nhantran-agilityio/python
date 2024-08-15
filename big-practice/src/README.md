# Django Big Practice - Student Management

## Overview
Build the simple Student Management app created with Python, Django, REST framework and SQLite. We can view detail requirement at [Link](https://docs.google.com/document/d/1JHRwU7X1Qqw5KF8nG7NHcQWsH0l4ZenITZtS6tc-zbE/edit?usp=sharing)

## Timeline
- Start day: *Aug 01, 2024*
- End day: *Aug 12, 2024*

- Estimate: 8 days
- Actual: 9 days

## Table of Contents
- [Technical Stack](#technical-stack)
- [Database model](#database-model)
- [Code Structure](#code-structure)
- [How To Run](#how-to-run)
- [Unit Testing](#unit-testing)
- [Coverage Reprot](#coverage-report)

## Technical Stack
- **Python 3.12**: Python programming language
- **Django 5.0.7**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework 3.15.2**: A powerful toolkit for building Web APIs in Django, enabling easy serialization and rendering of data.
- **SQlite**: SQLite is an in-process library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine

## Database model
  - [DB diagram](https://dbdiagram.io/d/Student-Management-66aa31698b4bb5230edb1111)

## Code structure
    ├── src/
    │   ├── accounts
    │   │   ├── migrations     <- contains database migration files generated
    │   │   ├── tests          <- define for performing tests user
    │   │   ├── admin.py       <- configures the Django admin interface for managing User models
    │   │   ├── apps.py        <- configuration for this application
    │   │   ├── models.py      <- defines User models.
    │   │   ├── serializers.py <- convert data types into a format
    │   │   ├── urls.py        <- define the URL routes
    │   │   └── views.py       <- controller functions for handling HTTP requests
    │   │
    │   ├── courses
    │   │   ├── migrations     <- contains database migration files generated
    │   │   ├── tests          <- define for performing tests user
    │   │   ├── admin.py       <- configures the Django admin interface for managing User models
    │   │   ├── apps.py        <- configuration for this application
    │   │   ├── models.py      <- defines User models.
    │   │   ├── serializers.py <- convert data types into a format
    │   │   ├── urls.py        <- define the URL routes
    │   │   └── views.py       <- controller functions for handling HTTP requests
    │   │
    │   ├── report
    │   │   ├── migrations     <- contains database migration files generated
    │   │   ├── tests          <- define for performing tests user
    │   │   ├── admin.py       <- configures the Django admin interface for managing User models
    │   │   ├── apps.py        <- configuration for this application
    │   │   ├── models.py      <- defines User models.
    │   │   ├── serializers.py <- convert data types into a format
    │   │   ├── urls.py        <- define the URL routes
    │   │   └── views.py       <- controller functions for handling HTTP requests
    │   │
    │   ├── student
    │   │   ├── migrations     <- contains database migration files generated
    │   │   ├── tests          <- define for performing tests user
    │   │   ├── admin.py       <- configures the Django admin interface for managing User models
    │   │   ├── apps.py        <- configuration for this application
    │   │   ├── models.py      <- defines User models.
    │   │   ├── serializers.py <- convert data types into a format
    │   │   ├── urls.py        <- define the URL routes
    │   │   └── views.py       <- controller functions for handling HTTP requests
    │   │
    │   ├── studentManagement
    │   │   └── settings.py    <-  settings and configuration for database, apps, templates, etc...
    │   │   └──  urls.py       <- URL routes for project, linking app routes
    │   │   ├── asgi.py        <- async web server configuration
    │   │   └── wsgi.py        <- sync web server configuration
    │
    ├── .gitignore
    ├── .editcongig
    ├── .coveragerc            <- Config test coverage
    ├── README.md
    ├── Dockerfile
    ├── .env.sample.py
    ├── manage.py              <- execute several commands at a project level
    ├── .flake8                <- checking the style and quality of Python code
    ├── requirements
    ├── .env.sample
    ├── .pre-commit-config.yaml
    └── docker-compose.yaml

## How to run
**Clone the repository**
```
git clone git@gitlab.asoft-python.com:nhan.tran/python-training.git
cd python-training/
git checkout feat/django-big-practice
```

## Admin Interface
**Admin can view all resources and have full permission on them.**
- Can CRUD, View all course, report, student, user
- Can search student by first name, last name and email
- Can filter student by course

[![admin-site.png](https://i.postimg.cc/P502LZwS/admin-site.png)](https://postimg.cc/68Ldg8zZ)
**APIs**
[![api.png](https://i.postimg.cc/hhFKtnmC/api.png)](https://postimg.cc/0KCTVLcm)



**Run with virtualenv at local environment**

1. Create a virtual environment:

```
python3 -m venv env
```

2. Activate the virtual environment
```
source env/bin/activate
```
3. Install dependencies from requirements.txt.

```
cd src
pip install -r requirements.txt
```

4. Run server
```
python manage.py runserver 8000
```

5. Browsable APIs

- Go to [http://0.0.0.0:8000/swagger/](http://0.0.0.0:8000/swagger/) to view all APIs.
- Go to Admin: [http://0.0.0.0:8000/admin/](http://0.0.0.0:8000/admin/)
   - Username/password: Admin/Abcd@1234

## Unit Testing
- coverage run manage.py test
- coverage report
- coverage html

## Coverage Report
```
Name                                 Stmts   Miss Branch BrPart  Cover
----------------------------------------------------------------------
accounts/models.py                       7      0      0      0   100%
accounts/views.py                       22      0      2      0   100%
courses/models.py                        8      0      0      0   100%
courses/views.py                         9      0      0      0   100%
report/models.py                        11      0      0      0   100%
report/views.py                         10      0      0      0   100%
student/filters.py                      21      0      2      0   100%
student/models.py                       43      0      6      0   100%
student/views.py                        14      0      0      0   100%
studentManagement/settings/base.py      23      0      0      0   100%
studentManagement/settings/dev.py        1      0      0      0   100%
studentManagement/settings/test.py       1      0      0      0   100%
----------------------------------------------------------------------
TOTAL                                  170      0     10      0   100%
```
