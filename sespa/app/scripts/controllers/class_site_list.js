'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:ClassSiteListCtrl
 * @description
 * # ClassSiteListCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('ClassSiteListCtrl', function (advisingData, advisingUtilities, $scope) {
    $scope.sortType = 'description';
    $scope.sortReverse = false;

    advisingData.classSites().then(function(class_sites) {
      $scope.classSites = class_sites;
    }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
    }, function(update) {
      advisingUtilities.updateProgress(update, $scope);
    });

  });
