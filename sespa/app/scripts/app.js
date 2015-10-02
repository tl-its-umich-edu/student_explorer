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
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl'
      })
      .when('/advisorList', {
        templateUrl: 'views/advisorList.html',
        controller: 'AdvisorcontrollerCtrl'
      })
      .when('/:advisor/studentList/', {
        templateUrl: 'views/studentList.html',
        controller: 'StudentcontrollerCtrl'
      })
      .when('/:advisor/studentDetail/:student/', {
        templateUrl: 'views/studentDetail.html',
        controller: 'StudentcontrollerCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
