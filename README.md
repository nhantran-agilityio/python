# Django Big Practice - Human Resource Management

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.0.7-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/djangorestframework-3.15.2-red.svg)](https://www.django-rest-framework.org/)
[![Sentry](https://img.shields.io/badge/sentry-0.23.4-blue.svg)](https://sentry.io/)
[![Caching in REST Framework](https://img.shields.io/badge/caching%20in%20REST%20Framework-yellow.svg)](https://www.django-rest-framework.org/api-guide/caching/)
[![Celery](https://img.shields.io/badge/celery-green.svg)](https://docs.celeryq.dev/en/stable/index.html)
[![Swagger](https://img.shields.io/badge/swagger-blue.svg)](https://swagger.io/)
[![Django Debug Toolbar](https://img.shields.io/badge/django%20debug%20toolbar-black.svg)](https://django-debug-toolbar.readthedocs.io/en/latest/)
![PostgreSQL](https://img.shields.io/badge/postgrestSQL-brightgreen.svg)

## Overview
A comprehensive human resource management system built with Rest Django and Django frames. This application helps organizations manage employees effectively by providing features such as employee profile management, leave application,...

## Features
- **User Authentication and Authorization**: Implement secure login and role-based access control for various user roles.
- **Employee Management**: Enable creation, updating, and deletion of employee profiles with ease.
- **Leave Application Management**: Manage leave applications with features to create, edit, delete, approve, decline, recall, and process recall requests.
- **Document Management**: Organize and manage employee-related documents efficiently.
- **Report Generation**: Generate detailed reports, including leave history and employee statistics, for better insights.
- **Background Tasks**: Leverage Celery for asynchronous task execution, including sending notifications and generating reports.
- **RESTful APIs**: Provide robust API endpoints for seamless integration with external systems.
- **Admin Interface**: Offer a user-friendly admin dashboard for managing resources and performing CRUD operations.
- **Statistics and Analytics**: Deliver dynamic insights and data visualizations to support informed decision-making.

## Timeline (March 12 to April 1, 2025)

- **Total Duration**: 14 days
- **Update Required**: 8 days

## Database Model

-   DB diagram: ![db.png](https://i.postimg.cc/ZRhFnVqx/Screenshot-2025-04-10-at-10-28-22.png)

## Deploy link

-  [Admin interface](https://human-resource.up.railway.app/admin/)
-  [Swagger](https://human-resource.up.railway.app/swagger/)


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
│   └── templates
│   │   └── activation_email.txt
├── contact
│   ├── migrations
│   ├── tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── guarantor
│   ├── migrations
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── job
│   └── django.log
├── job_responsibility
│   ├── migrations
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── kin
│   ├── migrations
│   ├── tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── leave_application
│   ├── migrations
│   ├── tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── notification
│   ├── migrations
│   ├── tests
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│   └── signals.py
├── config
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
├── tests
├── utils
├── .gitignore
├── .editorconfig
├── .coveragerc
├── README.md
├── .env.sample
├── manage.py
├── .flake8
├── .env.sample
├── .pre-commit-config.yaml
```

## How to Run

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git

### Clone the repository

```bash
git@gitlab.asoft-python.com:nhan.tran/human-resource.git
cd human-resource
git checkout dev
```

### Run with virtualenv in local environment

1. Create a virtual environment:

```bash
python3 -m venv env
```

2. Activate the virtual environment:

```bash
source env/bin/activate

3. Install dependencies:

```bash
cd src
pip install -r requirements/dev.txt
```

4. Set up environment variables:

```bash
cp .env.sample .env
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create superuser:

```bash
python manage.py createsuperuser
```

7. Run the server:

```bash
python manage.py runserver 8000
```

8. Access the application:

- [Swagger](http://0.0.0.0:8000/swagger/)
- [Redoc](http://0.0.0.0:8000/redoc/)
- [Admin](http://0.0.0.0:8000/admin/)

## Unit Testing

-   Run tests:

```
coverage run manage.py test
```
-   Generate coverage report:

```
coverage report

coverage html

-  Coverage: ![db.png](https://i.postimg.cc/d19hFqK3/Screenshot-2025-04-25-at-09-34-23.png)

```
