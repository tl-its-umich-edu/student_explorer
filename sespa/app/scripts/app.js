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
    'ui-rangeSlider',
    'nvd3ChartDirectives',
    'sespaFilters'
  ])
  .config(function($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/advisor_detail.html',
        controller: 'AdvisorDetailCtrl',
      })
      .when('/advisors/', {
        templateUrl: 'views/advisor_list.html',
        controller: 'AdvisorListCtrl',
      })
      .when('/advisors/:advisor/', {
        templateUrl: 'views/advisor_detail.html',
        controller: 'AdvisorDetailCtrl',
      })
      .when('/students/', {
        templateUrl: 'views/student_list.html',
        controller: 'StudentSearchCtrl',
      })
      .when('/students/:student/', {
        templateUrl: 'views/student_detail.html',
        controller: 'StudentDetailCtrl',
      })
      .when('/students/:student/class_sites/', {
        templateUrl: 'views/student_class_site_list.html',
        controller: 'StudentClassSiteListCtrl',
      })
      .when('/students/:student/class_sites/:classSiteCode/', {
        templateUrl: 'views/student_class_site_detail.html',
        controller: 'StudentClassSiteDetailCtrl',
      })
      .when('/students/:student/class_sites/:classSiteCode/assignments/', {
        redirectTo: '/students/:student/class_sites/:classSiteCode/',
      })
      .when('/students/:student/class_sites/:classSiteCode/history/', {
        redirectTo: '/students/:student/class_sites/:classSiteCode/',
      })
      .otherwise({
        redirectTo: '/'
      });
  });

/* Remove cache */
angular
  .module('sespaApp')
  .run(function($rootScope, $templateCache) {
   $rootScope.$on('$viewContentLoaded', function() {
      $templateCache.removeAll();
   });
});

/* Index nav bar*/
$('[data-toggle="collapse"]').on('click', function() { 
    $('li.active').removeClass('active');
    $(this).parent('li').addClass('active'); 
});
