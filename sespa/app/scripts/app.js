'use strict';

/**
 * @ngdoc overview
 * @name sespaApp
 * @description
 * # sespaApp
 *
 * Main module of the application.
 */
angular
  .module('sespaApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ngMaterial',
    'ui-rangeSlider'
  ])
  .config(function($routeProvider) {
    $routeProvider
      .when('/advisors', {
        templateUrl: 'views/advisor_list.html',
        controller: 'AdvisorListCtrl',
        controllerAs: 'ctrl',
      })
      .when('/students', {
        templateUrl: 'views/student_list.html',
        controller: 'StudentListCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
