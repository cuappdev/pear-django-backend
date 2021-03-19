# Pear Django Backend

A project by [Cornell AppDev](http://cornellappdev.com), a project team at Cornell University.

## Installation

This project uses the Django Rest Framework. 
Clone the project with

```
git clone https://github.com/cuappdev/pear-django.git
```

After cloning the project, `cd` into the new directory and install dependencies with

```
$ python3 -m pip install virtualenv venv
$ . venv/bin/activate
(venv) $ python3 -m pip install -r requirements.txt
```

You can run the project with

```
(venv) $ python3 manage.py runserver
```
You can update the database schema with
```
(venv) $ python3 manage.py makemigrations
(venv) $ python3 manage.py migrate
```

### Setting up database:
When running in local development, we will be using `db.sqlite3`. Check the Slack for production environment Postgres' environment variables.

### Environment Variables:

It is recommended to use [`direnv`](https://direnv.net). To set up, run the following:

```bash
cp envrc.template .envrc
```

## Configuration

The linter and import organizers are already installed in the pre-commit hook, so as long as you have your virtual environment activated (and have installed `requirements.txt`), your git commits will be parsed by these tools.
