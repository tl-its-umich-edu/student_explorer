'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:SespaAppCtrl
 * @description
 * # SespaAppCtrl
 * Controller of the sespaApp
 */

angular.module('sespaApp')
  .controller('SespaAppCtrl', function(advisingData, advisingUtilities, $scope, $location) {
    advisingData.config().then(function(config) {
      $scope.config = config;
      $scope.studentSearch = function() {
        $location.path('/students').search({
          search: $scope.search
        });
      };
    });

    advisingData.userInfo().then(function(userInfo) {
      $scope.userInfo = userInfo;
    }, function(reason) {
      console.log(reason);
      advisingUtilities.alert('You are not logged in! <a href="login/">Login</a>', 'danger');
    });
    
    $scope.isActive = function (viewLocation) { 
        return viewLocation === $location.path();
    };
  });
