# student explorer #

## Set up submodules ##
1. git submodule init
2. git submodule update

## Development Environment ##
1. Install Vagrant (https://www.vagrantup.com/)
2. `cd student_explorer`
3. `vagrant up`
4. `vagrant ssh`
    - `cd /vagrant/`
    - `python manage.py migrate`
    - `python manage.py loaddata */fixtures/*.json`
    - `python manage.py runserver`
5. Browse to [http://localhost:2080/](http://localhost:2080/)

## Configuring an external database ##
- Add an database to the DATABASES setting ('lt_dataset' in this example).
- Add any database routers to DATABASE_ROUTERS.
- Use ADVISING_DATABASE to specify the database name.
- If custom models are needed:
    - Add the package to the INSTALLED_APPS
    - Use ADVISING_PACKAGE to specify the package name.
