'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:AdvisorDetailCtrl
 * @description
 * # AdvisorDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('AdvisorDetailCtrl', function(advisingData, $scope) {
    $scope.selected = null;
    $scope.selectedName = window.location.href.split('/').slice(-1)[0];
    $scope.selectedAdStudent = null;
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;
    // $scope.searchAdvisor = '';
    // $scope.scroll = scroll;

    $scope.hasStatusData = false;
    $scope.hasGpaData = false;
    $scope.hasYearData = false;
    $scope.toAdvisorList = toAdvisorList;

    advisingData.advisorDetails($scope.selectedName).then(function(advisor) {
      $scope.selected = advisor;
    });

    advisingData.advisorsStudents($scope.selectedName).then(function(students) {
      $scope.selectedAdStudent = students;
      $scope.selectedAdStudent.some(function(student) {
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
      window.location.href = 'http://localhost:2080/#/advisors';
    }
  });
