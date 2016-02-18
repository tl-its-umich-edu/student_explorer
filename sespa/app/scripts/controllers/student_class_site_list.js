'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:ClassSiteListCtrl
 * @description
 * # ClassSiteListCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('StudentClassSiteListCtrl', function(advisingData, advisingUtilities, $scope, $routeParams) {
    $scope.classSiteListHeader = null;
    $scope.student = null;
    $scope.sortType = 'class_site.description';
    $scope.sortReverse = false;
    $scope.searchStudent = '';
    // $scope.scroll = scroll;

    $scope.classSites = [];

    advisingData.studentClassSites($routeParams.student).then(function(class_sites) {
      $scope.classSites = class_sites;
    }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
    });
    
    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.classSiteListHeader = student.first_name + ' ' + student.last_name;
      $scope.student = student;
    }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
    });
    
  });
