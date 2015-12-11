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
    $scope.advisors = null;
    $scope.mentors = null;
    $scope.classSites = null;
    $scope.sortTypeAdvisor = 'advisor.last_name';
    $scope.sortTypeMentor = 'mentor.last_name';
  	$scope.sortType = 'class_site.description';
    $scope.sortReverseAdvisor = false;
    $scope.sortReverseMentor = false;
    $scope.sortReverse = false;

  	advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.student = student;
    });
    
    advisingData.studentAdvisors($routeParams.student).then(function(advisors) {
      $scope.advisors = advisors;
    });
    
    advisingData.studentMentors($routeParams.student).then(function(mentors) {
      $scope.mentors = mentors;
    });
    
    advisingData.studentClassSites($routeParams.student).then(function(class_sites) {
      console.log(class_sites);
      $scope.classSites = class_sites;
    });

  });
