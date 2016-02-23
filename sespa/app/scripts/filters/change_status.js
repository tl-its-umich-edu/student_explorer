'use strict';

/**
 * @ngdoc filter
 * @name sespaApp.filter:changeStatus
 * @function
 * @description
 * # changeStatus
 * Filter in the sespaApp.
 */
angular.module('sespaApp')
  .filter('changeStatus', function () {
    return function (status) {
      return ({
        'green': 'Encourage',
        'yellow': 'Explore',
        'red': 'Engage',
        'above': 'The student scored at least 5 percentage points higher than the mean.',
        'near': 'The student scored within 5 percentage points of the mean.',
        'below': 'The student scored at least 5 percentage points lower than the mean.',
      }[String(status).toLowerCase()] || null);
    };
  });
