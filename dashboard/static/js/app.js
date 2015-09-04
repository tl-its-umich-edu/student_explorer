angular
  .module('studentexplorerApp', ['ngMaterial', 'students', 'data-table'])
  .config(function($mdThemingProvider){
    $mdThemingProvider.theme('default')
      .primaryPalette('indigo')
      .accentPalette('yellow');
    });