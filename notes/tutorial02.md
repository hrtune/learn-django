# The Database

Set up databases
* In `mysite/settings.py`, there is a variable `DATABASE`
	* ENGINE : choose the database engine from https://github.com/django/django/tree/main/django/db/backends
	* NAME : name of your database

Create models
```
polls/models.py
```
* Each class represents a model for the database.
* Each attribute for a model represents a field (column) for the model.

Activate models
* Add 'polls.apps.PollsConfig' into `INSTALLED_APPS` list in `settings.py`.

Make a migrations file and migrate
```sh
$ python manage.py makemigrations polls
```
```sh
$ python manage.py migrate
```

See SQL to run when migrate
```sh
$ python manage.py sqlmigrate polls 0001
```
* 0001 is an index number of migrations


