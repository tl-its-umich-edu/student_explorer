'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:StudentSearchCtrl
 * @description
 * # StudentSearchCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('StudentSearchCtrl', function($scope, advisingData, $routeParams) {
    $scope.studentListHeader = 'Search Students';
    $scope.selected = null;
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;

    $scope.students = [];

    var displayStudents = function(students) {
      $scope.students = students;
    };

    if (typeof $routeParams.search !== 'undefined') {
      advisingData.searchStudents($routeParams.search).then(displayStudents);
    }
  });
