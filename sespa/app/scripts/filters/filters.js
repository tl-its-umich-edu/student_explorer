'use strict';

angular.module('sespaFilters', []).filter('colorToStatus', function () {
  return function (status) {
    return ({
      'green': 'Encourage',
      'yellow': 'Explore',
      'red': 'Engage',
    }[String(status).toLowerCase()] || null);
  };
});
