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
        templateUrl: 'views/advisorList.html',
        controller: 'AdvisorCtrl'
      })
      .when('/advisors/:advisor', {
        templateUrl: 'views/studentList.html',
        controller: 'StudentCtrl'
      })
      .when('/advisors/:advisor/students/:student', {
        templateUrl: 'views/studentDetail.html',
        controller: 'StudentCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
