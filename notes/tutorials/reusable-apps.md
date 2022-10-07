# Reusable Apps

https://docs.djangoproject.com/en/4.1/intro/reusable-apps/

* The Python Package Index (PyPI) has a vast range of packages.
    * https://pypi.org/
* Likewise, for Django Packages: https://djangopackages.org/



## Packaging your apps

1. Create a parent directory `django-polls`  for polls, outside of your Django project.
2. Move the polls directory into the django-polls directory.
3. Create a file `django-polls/README.rst`
4. Create a `django-polls/LICENSE` file.
5. Create `pyproject.toml`, `setup.cfg`, and `setup.py` files.
    * cf. https://setuptools.pypa.io/en/latest/
6. Create a `MANIFEST.in` file.
7. Create a `django-polls/docs` directory for docs.
8. Try building your package with `python setup.py sdist` (run from inside django-polls).
    * This creates a directory called `dist` and builds your new package, `django-polls-0.1.tar.gz`.

## Use your own package

1. To install the package
```sh
$ python -m pip install --user django-polls/dist/django-polls-0.1.tar.gz
```
2. Check if it works
3. To uninstall
```sh
$ python -m pip uninstall django-polls
```


