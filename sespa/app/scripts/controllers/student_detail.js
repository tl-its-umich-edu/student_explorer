'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:StudentDetailCtrl
 * @description
 * # StudentDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('StudentDetailCtrl', function(advisingData, $scope, $routeParams) {
  	$scope.student = null;
  	$scope.sortType = 'class_site';
  	$scope.advisors = null;
    $scope.courses = null;

  	advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.student = student;
    });
    
    advisingData.studentAdvisors($routeParams.student).then(function(advisors){
        $scope.advisors = advisors;
    });
    
    advisingData.studentCourses($routeParams.student).then(function(course) {
      $scope.courses = course;
    });

  });
