'use strict';

angular.module('sespaFilters', []).filter('colorToStatus', function () {
  return function (statusOutput) {
    return ({
      'green': 'Encourage',
      'yellow': 'Explore',
      'red': 'Engage',
    }[String(statusOutput).toLowerCase()] || 'Experimental');
  };
});
