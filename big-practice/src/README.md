# Django Big Practice - Student Management

## Overview

Build a simple Student Management app using Python, Django, REST framework, and SQLite. Detailed requirements can be found in the project documentation.

## Timeline

-   Basic: 8 days
-   Advanced: 10 days

## Table of Contents

-   [Technical Stack](#technical-stack)
-   [Database Model](#database-model)
-   [Code Structure](#code-structure)
-   [How to Run](#how-to-run)
-   [Admin Interface](#admin-interface)
-   [APIs](#apis)
-   [Advanced Features](#advanced-features)
-   [Unit Testing](#unit-testing)
-   [Coverage Report](#coverage-report)

## Technical Stack

-   **Python 3.12**: Python programming language
-   **Django 5.0.7**: A high-level Python web framework
-   **Django REST Framework 3.15.2**: Toolkit for building Web APIs in Django
-   **SQLite**: Self-contained, serverless, zero-configuration SQL database engine

## Database Model

-   DB diagram: ![db.png](https://i.postimg.cc/TPGv0tH2/Screenshot-2025-02-17-at-18-12-15.png)

## Code Structure

```
src/
├── accounts
│   ├── migrations
│   ├── tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── courses
│   ├── migrations
│   ├── tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── instructors
│   ├── migrations
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── logs
│   └── django.log
├── notifications
│   ├── migrations
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── report
│   ├── migrations
│   ├── tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── student
│   ├── migrations
│   ├── tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── studentManagement
│   └── settings
│       ├── base.py
│       ├── dev.py
│       ├── production.py
│       ├── test.py
│   ├── __init__.py
│   ├── celery.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .gitignore
├── .editorconfig
├── .coveragerc
├── README.md
├── Dockerfile
├── .env.sample
├── manage.py
├── .flake8
├── requirements.txt
├── .env.sample
├── .pre-commit-config.yaml
└── docker-compose.yaml
```

## How to Run

**Clone the repository**

```
git clone git@example.com:your-username/your-repository.git
cd python-training/
git checkout feat/django-big-practice
```

**Run with virtualenv in local environment**

1. Create a virtual environment:

```
python3 -m venv env
```

2. Activate the virtual environment:

```
source env/bin/activate
```

3. Install dependencies:

```
cd src
pip install -r requirements.txt
```

4. Run the server:

```
python manage.py runserver 8000
```

5. Access APIs:

-   [Swagger](http://0.0.0.0:8000/swagger/)
-   [Admin](http://0.0.0.0:8000/admin/)
    -   Set up an admin account by running the following command:
        ```
        python manage.py createsuperuser
        ```

## Admin Interface

**Admin can view all resources and have full permissions.**

-   CRUD operations on courses, reports, students, and users
-   Search students by first name, last name, and email
-   Filter students by course

![admin-site.png](https://i.postimg.cc/P502LZwS/admin-site.png)

## APIs

-   Authentication
    -   Login
    -   Sign Up
-   CRUD operations on Student, Course, Report
-   Filtering
    - View detailed information of a student/course
    - List students
    - Order by first name
    - Search students by name or email
    - Search students by birth date range
-   List Courses
    -   All information of students by course
    -   Total number of students by course
    -   Apply pagination for all listing APIs

![api.png](https://i.postimg.cc/hhFKtnmC/api.png)

## Advanced Features

-   Email confirmation for registration and password reset
-   Auto-enrollment in introductory courses for new users
-   Dynamic statistics like average enrollments or top courses
-   Background tasks (asynchronous)
    -   Send a welcome email upon successful registration
    -   Notify instructors if a course reaches enrollment limit
-   Notifications
    -   Users can see a list of notifications in their dashboard
    -   Notify instructors when a student enrolls in a course
    -   Notify students when they are removed from a course
-   Scheduling
    -   Weekly clean-up of inactive courses (3 months)
    -   Monthly report (CSV) sent to instructors about enrolled students per course
-   Monitoring, testing, and deployment
    -   Set up logging and monitoring (e.g., Sentry)

## Unit Testing

-   Run tests:

```
coverage run manage.py test
```

-   Generate coverage report:

```
coverage report
coverage html
```

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
