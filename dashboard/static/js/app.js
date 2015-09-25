angular
  .module('studentexplorerApp', ['ngMaterial', 'students', 'advisors', 'ui-rangeSlider'])
  .config(function($mdThemingProvider){
    $mdThemingProvider.theme('default')
      .primaryPalette('indigo')
      .accentPalette('yellow');
    });