'use strict';

/**
 * @ngdoc service
 * @name sespaApp.advisingUtilities
 * @description
 * # advisingUtilities
 * Factory in the sespaApp.
 */
angular.module('sespaApp')
  .factory('advisingUtilities', function () {
    // Service logic

    // Public API here
    return {
      updateProgress: function(update, $scope) {
        if (typeof update === 'number') {
          $scope.progress = update * 100;
        }
      },
    };
  });
