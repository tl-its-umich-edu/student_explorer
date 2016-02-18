'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:ClassSiteDetailCtrl
 * @description
 * # ClassSiteDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('ClassSiteDetailCtrl', function (advisingData, advisingUtilities, $scope, $routeParams) {
    advisingData.classSiteDetails($routeParams.classSiteCode).then(function(classSite) {
      $scope.classSite = classSite;
    }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope, true);
    });
  });
