'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:AdvisorListCtrl
 * @description
 * # AdvisorListCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('AdvisorListCtrl', function(advisingData, $scope) {
    $scope.selected = null;
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;
    $scope.searchAdvisor = '';
    $scope.scroll = scroll;

    advisingData.allAdvisors().then(function(advisors) {
      $scope.advisors = advisors;
    });
  });
