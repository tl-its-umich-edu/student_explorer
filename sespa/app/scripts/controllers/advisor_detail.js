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

    advisingData.userInfo().then(function(userInfo) {
      var advisorUsername;
      $scope.username = userInfo.username;
      if (typeof $routeParams.advisor === 'undefined') {
        advisorUsername = userInfo.username;
      } else {
        advisorUsername = $routeParams.advisor;
      }

      advisingData.advisorDetails(advisorUsername).then(function(advisor) {
        $scope.advisor = advisor;
      }, function(reason) {
        console.log(reason);
      });

      advisingData.advisorsStudents(advisorUsername).then(function(students) {
        $scope.progress = 100;
        $scope.students = students;
      }, function(reason) {
        advisingUtilities.httpErrorHandler(reason);
      }, function(update) {
        advisingUtilities.updateProgress(update, $scope);
      });

    });
  });
