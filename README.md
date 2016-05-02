# student explorer #

## Set up submodules ##
1. git submodule init
2. git submodule update

## Development Environment ##

### First Time Setup ###
1. Install Vagrant (https://www.vagrantup.com/)
2. Start Vagrant
   - `cd student_explorer`
   - `vagrant up`
   - `vagrant ssh`
3. Install bower
   - `cd /vagrant/sespa`
   - `bower install`

### Regular Use ###
1. Initialize and start app server
    - `cd /vagrant`
    - `python manage.py migrate` (updates your repo if anything as changed)
    - `python manage.py loaddata seumich/fixtures/dev_data.json student_explorer/fixtures/dev_users.json` (loads some test student data)
    - `python manage.py runserver`
2. Browse to [http://localhost:2080/login/](http://localhost:2080/login/)
    - Login as individual advisors using their lower-case first name as username/password (e.g.: burl/burl)
    - Student with useful data: [http://localhost:2080/#/students/grace/](http://localhost:2080/#/students/grace/)

## Configuring an external database ##
- Add an database to the DATABASES setting ('lt_dataset' in this example).
- Add any database routers to DATABASE_ROUTERS.
- Use ADVISING_DATABASE to specify the database name.
- If custom models are needed:
    - Add the package to the INSTALLED_APPS
    - Use ADVISING_PACKAGE to specify the package name.

## Update Data Fixtures ##

This is the procedure to add dummy data to the fixture files.

- Connect to the database in the Vagrant VM. (This can be done from your host system via the port defined in the Vagrant file, 2033)
- Delete all tables.
- Run the migrations to recreate the tables: `python manage.py migrate`
- Run the loaddata command to load existing fixtures: `python manage.py loaddata */fixtures/*.json`
- Make changes to the database.
- Save the changes to a fixture file: `python manage.py dumpdata --indent 4 advising > advising/fixtures/dev_data.json`
- Commit the changes to the updated fixture file.
