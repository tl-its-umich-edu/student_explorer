'use strict';

/**
 * @ngdoc service
 * @name sespaApp.StudentExplorerApiService
 * @description
 * # StudentExplorerApiService
 * Factory in the sespaApp.
 */
angular.module('sespaApp')
  .factory('StudentExplorerApiService', function () {
    // Service logic
    // ...

    var meaningOfLife = 42;

    // Public API here
    return {
      someMethod: function () {
        return meaningOfLife;
      }
    };
  });
