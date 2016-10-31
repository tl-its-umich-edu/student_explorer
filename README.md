# Student Explorer #

## Development Environment ##

### Setup ###
1. Install [Vagrant](https://www.vagrantup.com/)
2. Follow steps in the "Run development server" section below. The `vagrant up` step should run the provision script on its first run.

### Run development server ###
- `cd student_explorer`
- `vagrant up`
- `vagrant ssh`
- `cd /vagrant`
- `python manage.py runserver`
- Browse to [http://localhost:2082/](http://localhost:2082/)
- Login as individual advisors using their lower-case first name as username/password (e.g.: burl/burl)
- Student with useful data: [http://localhost:2082/students/grace/](http://localhost:2082/students/grace/)

### Using the Django Debug Toolbar ###
For the [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/1.5/) to work in development, please add the following in _student_explorer > local > settings_override.py_
- `INSTALLED_APPS += ('debug_toolbar',)`
- `MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)`
- `DEBUG_TOOLBAR_PATCH_SETTINGS = False`
- `INTERNAL_IPS = ['10.0.2.2']`

### Note on settings ###
By default manage.py looks for the student_explorer.local.settings_override module. This file is created manually as documented in the setup steps above.

By default wsgi.py (which is used by start.sh) looks for the student_explorer.settings module. This file is versioned as part of this repository.

This behavior can be changed for both manage.py and wsgi.py by setting the DJANGO_SETTINGS_MODULE environment variable.