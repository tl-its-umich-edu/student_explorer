'use strict';

/**
 * @ngdoc filter
 * @name sespaApp.filter:filter
 * @function
 * @description
 * # filter
 * Filter in the sespaApp.
 */
angular.module('sespaApp')
  .filter('colorToStatus', function () {
    return function (status) {
      return ({
        'green': 'Encourage',
        'yellow': 'Explore',
        'red': 'Engage',
      }[String(status).toLowerCase()] || null);
    };
  });
