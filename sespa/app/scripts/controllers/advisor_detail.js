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
    // $scope.sortType = 'last_name';
    // $scope.sortReverse = false;
    // $scope.searchAdvisor = '';
    // $scope.scroll = scroll;

    advisingData.advisorDetails($scope.selected).then(function(advisor) {
      $scope.advisors = advisor;
    });
  });
