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
    $scope.hasAdvisorProfile = true;

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
        if (reason.status === 404) {
          $scope.hasAdvisorProfile = false;
        } else {
          advisingUtilities.httpErrorHandler(reason, $scope);
        }
      });

      advisingData.advisorsStudents(advisorUsername).then(function(students) {
        $scope.progress = 100;
        $scope.students = students;
      }, function(reason) {
        if (reason.status !== 404) {
          advisingUtilities.httpErrorHandler(reason, $scope);
        }
      }, function(update) {
        advisingUtilities.updateProgress(update, $scope);
      });

    });
  });
