# sespa

This project is generated with [yo angular generator](https://github.com/yeoman/generator-angular)
version 0.11.1.

## Setup

### Install dependencies

    sudo apt-get install --yes git
    curl --silent --location https://deb.nodesource.com/setup_4.x | sudo bash -
    sudo apt-get install --yes nodejs
    sudo npm install --global npm@latest

### Install Bower

    sudo npm install --global bower

### Install Bower components

    cd sespa
    bower install

The interface should be working after this step.

### Install Grunt

    sudo npm install --global grunt-cli
    cd sespa
    npm install

### Add components

    bower install --save bower-package
    grunt wiredep
    
### Create production build

    grunt build

### Install Yeoman and the Angular generator

    sudo npm install --global yo
    sudo npm install --global generator-karma
    sudo npm install --global generator-angular

### Add Angular components

    yo angular:service

## Build & development

Run `grunt` for building and `grunt serve` for preview.

## Testing

Running `grunt test` will run the unit tests with karma.
