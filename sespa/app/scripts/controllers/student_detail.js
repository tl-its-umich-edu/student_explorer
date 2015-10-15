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

  	advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.student = student;
      $scope.advisors = student.advisors;
    });

  });
