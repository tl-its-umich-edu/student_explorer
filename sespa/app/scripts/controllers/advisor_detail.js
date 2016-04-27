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
    $scope.advisorUsername = null;
    $scope.advisor = null;
    $scope.students = null;
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;
    $scope.progress = 0;
    $scope.hasAdvisorProfile = true;
    $scope.filterStudentCourseStatus = function(status, name) {
      if (status === 'No data') {
        return 'No data';
      } else {
        return name + ': ' + status;
      }
    };

    advisingData.userInfo().then(function(userInfo) {
      if (typeof $routeParams.advisor === 'undefined') {
        // handle the current user case
        $scope.advisorUsername = userInfo.username;
      } else {
        $scope.advisorUsername = $routeParams.advisor;
      }

      advisingData.advisorDetails($scope.advisorUsername).then(function(advisor) {
        $scope.advisor = advisor;
      }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope, true);
      });

      advisingData.advisorsStudents($scope.advisorUsername).then(function(students) {
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
