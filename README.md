# student explorer #

## Development Environment ##
1. Install Vagrant (https://www.vagrantup.com/)
2. `cd student_explorer`
3. `vagrant up`
4. `vagrant ssh -c 'python /vagrant/manage.py migrate'`
5. `vagrant ssh -c 'python /vagrant/manage.py runserver'`
6. `vagrant ssh -c 'python /vagrant/manage.py loaddata advising/fixtures/*.json'`
7. Browse to [http://localhost:2080/](http://localhost:2080/)
