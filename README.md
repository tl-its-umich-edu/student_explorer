# Student Explorer #

## Development Environment ##

### Setup ###
1. Install [Vagrant](https://www.vagrantup.com/)
2. Start Vagrant
  - `cd student_explorer`
  - `vagrant up`
  - `vagrant ssh`
  - `cd /vagrant`
3. Setup development environment
  - `touch student_explorer/local/__init__.py`
  - `echo 'from student_explorer.settings import *' > student_explorer/local/settings.py`
4. Setup database
  - `python manage.py migrate` (updates your repo if anything as changed)
  - `python manage.py loaddata student_explorer/fixtures/dev_users.json` (loads some test user data)
  - `mysql -h 127.0.0.1 -u student_explorer -pstudent_explorer student_explorer < seumich/fixtures/dev_data_drop_create_and_insert.sql` (loads some test advising data)

### Run development server ###
  - `python manage.py runserver`
  - Browse to [http://localhost:2082/](http://localhost:2082/)
  - Login as individual advisors using their lower-case first name as username/password (e.g.: burl/burl)
  - Student with useful data: [http://localhost:2082/students/grace/](http://localhost:2082/students/grace/)
