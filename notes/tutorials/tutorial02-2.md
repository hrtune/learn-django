# Django Admin

Create an admin user
```sh
$ python manage.py createsuperuser
```
* The interactive session starts to register an admin

Register a model to the admin
`polls/admin.py`
```python
# ...
admin.site.register(Question)
```

Default address to the admin
```
/admin/
```


