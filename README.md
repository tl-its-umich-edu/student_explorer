# student explorer #

## Development Environment ##
1. Install Vagrant (https://www.vagrantup.com/)
2. `cd student_explorer`
3. `vagrant up`
4. `vagrant ssh`
    - `cd /vagrant/`
    - `python manage.py migrate`
    - `python manage.py createsuperuser`
    - `python manage.py loaddata advising/fixtures/*.json`
    - `python manage.py runserver`
7. Browse to [http://localhost:2080/](http://localhost:2080/)
