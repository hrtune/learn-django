# Set-ups

document : https://docs.djangoproject.com/en/4.1/intro/tutorial01/

---

Know django version
```sh
$ python -m django --version
```

---

Create a django project
```sh
$ django-admin startproject mysite
```
* where 'mysite' is the project name.

---

Initial files
```
mysite/                 <- root of the project
    manage.py          <- command line utility
    mysite/
        __init__.py   <- let python know the cd is a python module
        settings.py  <- configuration file for this django project
        urls.py     <- for routing requests
        asgi.py    <- An entry-point for ASGI-compatible web servers to serve your project.
        wsgi.py    <- An entry-point for WSGI-compatible web servers to serve your project.
```

---

Run the server
```sh
$ python manage.py runserver
```
* `$ python manage.py runserver 8080` where the '8080' is the port number.

---

Start app
```sh
$ python manage.py startapp polls
```
* where 'polls' is the app name

---

Write the simplest view (Coding starts from here!!)
```
polls/view.py
```

---

Edit urls.py to route the response
```
polls/urls.py
```

---

Edit mysite/urls.py to include the urls in polls
```
mysite/urls.py
```
