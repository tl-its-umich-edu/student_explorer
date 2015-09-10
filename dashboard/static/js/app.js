angular
  .module('studentexplorerApp', ['ngMaterial', 'students'])
  .config(function($mdThemingProvider){
    $mdThemingProvider.theme('default')
      .primaryPalette('indigo')
      .accentPalette('yellow');
    });