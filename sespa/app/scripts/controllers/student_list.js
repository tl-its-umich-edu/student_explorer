'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:StudentListCtrl
 * @description
 * # StudentListCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('StudentListCtrl', function(advisingData, $scope) {
    $scope.studentListHeader = 'All Students';
    $scope.selected = null;
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;
    $scope.searchStudent = '';
    // $scope.scroll = scroll;

    $scope.hasStatusData = false;
    $scope.hasGpaData = false;
    $scope.hasYearData = false;

    $scope.students = [];
    advisingData.allStudents().then(function(students) {
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
    });
  });
