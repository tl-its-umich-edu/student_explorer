'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:SespaAppCtrl
 * @description
 * # SespaAppCtrl
 * Controller of the sespaApp
 */

angular.module('sespaApp')
  .controller('SespaAppCtrl', function(advisingData, $scope) {
    advisingData.config().then(function(config) {
      $scope.config = config;
    });
  });
