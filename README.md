# student explorer #

## Development Environment ##
1. Install Vagrant (https://www.vagrantup.com/)
2. `cd student_explorer`
3. `vagrant up`
4. `vagrant ssh -c 'python /vagrant/manage.py migrate'`
5. `vagrant ssh -c 'python /vagrant/manage.py runserver'`
6. Browse to [http://localhost:8002/](http://localhost:8002/)
