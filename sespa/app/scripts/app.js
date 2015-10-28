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
      .when('/advisors', {
        templateUrl: 'views/advisor_list.html',
        controller: 'AdvisorListCtrl',
        controllerAs: 'ctrl',
      })
      .when('/advisors/:advisor', {
        templateUrl: 'views/advisor_detail.html',
        controller: 'AdvisorDetailCtrl',
        controllerAs: 'ctrl',
      })
      .when('/', {
        templateUrl: 'views/advisor_detail.html',
        controller: 'AdvisorDetailCtrl',
        controllerAs: 'ctrl',
      })
      .when('/students', {
        templateUrl: 'views/student_list.html',
        controller: 'StudentListCtrl'
      })
      .when('/students/:student', {
        templateUrl: 'views/student_detail.html',
        controller: 'StudentDetailCtrl',
        controllerAs: 'ctrl',
      })
      .otherwise({
        redirectTo: '/'
      });
  });
