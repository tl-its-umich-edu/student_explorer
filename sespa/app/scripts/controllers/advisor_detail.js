'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:AdvisorDetailCtrl
 * @description
 * # AdvisorDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('AdvisorDetailCtrl', function(advisingData, advisingUtilities, $scope, $routeParams) {
    $scope.advisor = null;
    $scope.students = null;
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;
    $scope.progress = 0;

    // $scope.searchAdvisor = '';
    // $scope.scroll = scroll;

    advisingData.advisorDetails($routeParams.advisor).then(function(advisor) {
      $scope.advisor = advisor;
    }, function(reason) {
      // window.alert(reason);
      appendAlert(reason);
    });

    advisingData.advisorsStudents($routeParams.advisor).then(function(students) {
      $scope.progress = 100;
      $scope.students = students;
    }, function(reason) {
      // window.alert(reason);
      appendAlert(reason);
    }, function(update) {
      advisingUtilities.updateProgress(update, $scope);
    });

  });
