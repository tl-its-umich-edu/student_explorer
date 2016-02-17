'use strict';

angular.module('sespaFilters', []).filter('colorToStatus', function () {
  return function (status) {
    return ({
      'green': 'Encourage',
      'yellow': 'Explore',
      'red': 'Engage',
    }[String(status).toLowerCase()] || null);
  };
}).filter('unique', function () {
  return function (items, attr) {
    var seen = {};
    return items.filter(function (item) {
      return (angular.isUndefined(attr) || !item.hasOwnProperty(attr))
        ? true
        : seen[item[attr]] = !seen[item[attr]];
    });
  };
});
