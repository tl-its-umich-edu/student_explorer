'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:StudentListCtrl
 * @description
 * # StudentListCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('StudentListCtrl', function(advisingData, $scope, $routeParams) {
    $scope.studentListHeader = 'All Students';
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;
    $scope.searchStudent = '';
    // $scope.scroll = scroll;

    $scope.students = [];

    var displayStudents = function(students) {
      $scope.students = students;
    };

    advisingData.searchStudents($routeParams.search).then(displayStudents);
  });
