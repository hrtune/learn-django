# Admins

## Customize the admin form

`polls/admin.py`
```python
class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

admin.site.register(Question, QuestionAdmin)
```

* `ModelAdmin.fields` is a list of  fields to show in the admin.
    * cf. https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fields
* `AdminSite.register(model_or_iterable, admin_class)`
    * registers `model` using `admin_class` to the admin.


```python
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
```

* The first element in a tuple is a title for the field.

```python
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
```

* Instead of registering the `Choice` model, this makes `Choice` editable in
    the `Question` form.
* The alternative `admin.TabularInLine` make the in-line edit tabular.

## Customize the admin change list

Add columns to the change list
```python
class QuestionAdmin(admin.ModelAdmin):
    # ...
    list_display = ('question_text', 'pub_date')
```

Use the display decorator
```python
class Question(models.Model):
    # ...
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    list_filter = ['pub_date']
    search_fields = ['question_text']
```

* cf. https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
* `list_filter` adds the filter for specified fields.
* `search_fields` adds the search box for specified fields.

## Customize the admin look and feel

Set the templates directory for the project
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
* What the heck is the division operator in the entry; `'DIRS': [BASE_DIR / 'templates']`.
    * 'DIRS' is a search path
Look up the django source files
```sh
$ python -c "import django; print(django.__path__)"
```

Then get `django/contrib/admin/templates/base_site.html`, copy it to
`templates/admin/base_site.html`.

Edit the `base_site.html` to override the default admin looks.

* Any of Django’s default admin templates can be overridden.




