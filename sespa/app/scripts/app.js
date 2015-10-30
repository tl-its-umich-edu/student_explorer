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
    'ui-rangeSlider'
  ])
  .config(function($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/advisor_detail.html',
        controller: 'AdvisorDetailCtrl',
      })
      .when('/advisors', {
        templateUrl: 'views/advisor_list.html',
        controller: 'AdvisorListCtrl',
      })
      .when('/advisors/:advisor', {
        templateUrl: 'views/advisor_detail.html',
        controller: 'AdvisorDetailCtrl',
      })
      .when('/students/:student', {
        templateUrl: 'views/student_detail.html',
        controller: 'StudentDetailCtrl',
      })
      .otherwise({
        redirectTo: '/'
      });
  });
