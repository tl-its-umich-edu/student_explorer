'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:AdvisorDetailCtrl
 * @description
 * # AdvisorDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('AdvisorDetailCtrl', function(advisingData, $scope, $routeParams, $location) {
    $scope.advisor = null;
    $scope.students = null;
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;
    // $scope.searchAdvisor = '';
    // $scope.scroll = scroll;

    $scope.toAdvisorList = toAdvisorList;

    advisingData.advisorDetails($routeParams.advisor).then(function(advisor) {
      $scope.advisor = advisor;
    });

    advisingData.advisorsStudents($routeParams.advisor).then(function(students) {
      $scope.students = students;
    })

    function toAdvisorList() {
      $location.path('/advisors/').replace();
    }
  });
