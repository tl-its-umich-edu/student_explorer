'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:StudentSearchCtrl
 * @description
 * # StudentSearchCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('StudentSearchCtrl', function($scope, advisingData, advisingUtilities, $routeParams, $location) {
    $scope.studentListHeader = 'Search Students';
    $scope.selected = null;
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;

    var displayStudents = function(students) {
      $scope.students = students;
    };

    if (typeof $routeParams.search !== 'undefined') {
      $scope.$parent.search = $routeParams.search;
      $scope.progress = 100;
      advisingData.searchStudents($routeParams.search).then(displayStudents, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
      }, function(update) {
        advisingUtilities.updateProgress(update, $scope);
      });
    } else if (typeof $routeParams.univ_id !== 'undefined') {
      // When filtering for a student, check to see if any student matches the filter terms.
      // Then redirect the user to that student's page. If no student matches, show an error.
      $scope.progress = 100;
      advisingData.filterStudents({
        'univ_id': $routeParams.univ_id
      }).then(function(data) {
        if (data.length === 1) {
          $location.path('/students/' + data[0].username + '/').search('univ_id', null).replace();
        } else {
          displayStudents(data);
        }
      }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
      }, function(update) {
        advisingUtilities.updateProgress(update, $scope);
      });
    } else {
      displayStudents([]);
    }
  });
