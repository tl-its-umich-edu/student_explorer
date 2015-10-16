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

    $scope.hasStatusData = false;
    $scope.hasGpaData = false;
    $scope.hasYearData = false;
    $scope.toAdvisorList = toAdvisorList;

    advisingData.advisorDetails($routeParams.advisor).then(function(advisor) {
      $scope.advisor = advisor;
    });

    advisingData.advisorsStudents($routeParams.advisor).then(function(students) {
      $scope.students = students;
      $scope.students.some(function(student) {
        if (student.statuses.length > 0) {
          $scope.hasStatusData = true;
        }
        if (student.gpa != null) {
          $scope.hasGpaData = true;
        }
        if (student.year != null) {
          $scope.hasYearData = true;
        }
        return $scope.hasStatusData == true && $scope.hasGPAData == true && $scope.hasYearData == true;
      });
    })

    function toAdvisorList() {
      $location.path('/advisors/').replace();
    }
  });
