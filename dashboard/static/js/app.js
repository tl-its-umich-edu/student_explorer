angular
  .module('studentexplorerApp', ['ngMaterial', 'students', 'ui-rangeSlider'])
  .config(function($mdThemingProvider){
    $mdThemingProvider.theme('default')
      .primaryPalette('indigo')
      .accentPalette('yellow');
    });