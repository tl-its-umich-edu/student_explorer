# sespa

This project is generated with [yo angular generator](https://github.com/yeoman/generator-angular)
version 0.11.1.

## Setup

Install dependencies.

    sudo apt-get install --yes git
    curl --silent --location https://deb.nodesource.com/setup_4.x | sudo bash -
    sudo apt-get install --yes nodejs
    sudo npm install --global npm@latest
    sudo npm install --global bower

Install components and modules

    cd sespa
    bower install
    
Add components

    sudo npm install --global grunt-cli
    npm install

    bower install --save bower-package
    grunt wiredep
    
Create production build

    grunt build

## Build & development

Run `grunt` for building and `grunt serve` for preview.

## Testing

Running `grunt test` will run the unit tests with karma.
