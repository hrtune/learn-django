# The Database

Set up databases
* In `mysite/settings.py`, there is a variable `DATABASE`
	* ENGINE : choose the database engine from https://github.com/django/django/tree/main/django/db/backends
	* NAME : name of your database

---

Create models
```
polls/models.py
```
* Each class represents a model for the database.
* Each attribute for a model represents a field (column) for the model.

---

Activate models
* Add 'polls.apps.PollsConfig' into `INSTALLED_APPS` list in `settings.py`.

Make a migrations file and migrate
```sh
$ python manage.py makemigrations polls
```
```sh
$ python manage.py migrate
```

---

See SQL to run when migrate
```sh
$ python manage.py sqlmigrate polls 0001
```
* 0001 is an index number of migrations

---

Run shell of django
```sh
$ python manage.py shell
```

---

Run python commands to create objects
c.f. https://docs.djangoproject.com/en/4.1/topics/db/queries/
```python

from polls.models import Choice, Question # import models

Question.objects.all() # show all objects in the table

# We need the timezone module (c.f. https://docs.djangoproject.com/en/4.1/ref/utils/#django.utils.timezone.now )
from django.utils import timezone

q = Question(question_text="What's new?", pub_date=timezone.now()) # make a question object in the memory (not in the database)
q.save() # save the object into the database
q.id # id has assigned for the object

# Show attributes of the object
q.question_text
q.pub_date

# Change the value
q.question_text = "What's up?"
q.save() # Don't forget to save

```

---

Define a `__str__()` method for each model
```
polls/models.py
```

---

Add a custom method to a model
```
polls/models.py
```
```python
class Question(models.Model):
    # ...
    def was_published_recently(self):
			#...
```
* I think this registers the method itself to the model... (Maybe)

---

More shell commands
```python
# ...
# filtering
Question.objects.filter(id=1) # filter by an id attribute
Question.objects.filter(question_text__startswith='What') # This is weird. Here is an option `__startswith`

from django.utils import timezone
current_year = timezone.now().year
Question.objects.get(pub_date__year=current_year) # Here also is an option `__year`

q = Question.objects.get(pk=1) # pk means `primary key`
q.was_published_recently() # call a method

# choices related to a question in q
q.choice_set.all()
q.choice_set.create(choice_text='Not much', votes=0)
c = q.choice_set.create(choice_text='Just hacking again', votes=0)
c.question
q.choice_set.count()

# Look above.  q.choice_set is a weird object because we never defined a choice_set attribute in the Question.
# I am not the only person... c.f. https://stackoverflow.com/questions/2048777/what-is-choice-set-in-this-django-app-tutorial

# Delete a choice
c = q.choice_set.filter(choice_text__startswith='Just hacking')
c.delete()
```



