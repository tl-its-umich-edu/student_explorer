# Student Explorer #

## Development Environment ##

### Setup ###
1. Install [Docker](https://www.docker.com/)
2. Follow steps in the "Run development server" section below.

### Run development server ###
- If you intend to do local development you should install and use docker-sync
  - See the directions here for installing the gem https://docker-sync.readthedocs.io/en/latest/getting-started/installation.html
  - If you can execute `docker-sync` you're good to go!
- `cd student_explorer`
- `docker-compose down; docker-compose build;`
- Either run 
  - `docker-sync start` if you want to be able to modify files (dev)
  - `docker-compose up -d` if you don't want to modify files (prod) 
- Browse to [http://localhost:2082/](http://localhost:2082/)
- Login as individual advisors using their lower-case first name as username/password (e.g.: burl/burl)
- Student with useful data: [http://localhost:2082/students/grace/](http://localhost:2082/students/grace/)

### Running the unit tests
- You should periodically run the unit tests and keep these updated. These have to be up when the server is up.
- `docker exec -it student_explorer /bin/bash -c "echo yes | python manage.py test"`

### Using the Django Debug Toolbar ###
For the [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/1.5/) to work in development. This is configured to only display if DEBUG=True and the logged in user is an admin.

### Note on settings ###
By default manage.py looks for the student_explorer.local.settings_override module. This file is created manually as documented in the setup steps above.

By default wsgi.py (which is used by start.sh) looks for the student_explorer.settings module. This file is versioned as part of this repository.

This behavior can be changed for both manage.py and wsgi.py by setting the DJANGO_SETTINGS_MODULE environment variable.

### Cron JOB
Users and files are loaded now with the cron job. This is run on a separate pod in Openshift when the environment variable IS_CRON_POD=true.

Crons are configured in this project with django-cron. Django-cron is executed whenever python manage.py runcrons is run but it is limited via a few environment variables.

The installation notes recommends that you have a Unix crontab scheduled to run every 5 minutes to run this command. https://django-cron.readthedocs.io/en/latest/installation.html

For local testing, make sure your secrets are added and your VPN is active. Then run this command on a running container to execute the cronjob

`docker exec -it student_explorer /bin/bash -c "python manage.py migrate django_cron && python manage.py runcrons --force"`
