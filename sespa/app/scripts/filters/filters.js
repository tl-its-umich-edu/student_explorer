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
  })
  .filter('relativeToMeanDesc', function () {
    return function (status) {
      return ({
        'above': 'The student scored at least 5 percentage points higher than the mean.',
        'near': 'The student scored within 5 percentage points of the mean.',
        'below': 'The student scored at least 5 percentage points lower than the mean.',
      }[String(status).toLowerCase()] || null);
    };
  });
