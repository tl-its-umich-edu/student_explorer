'use strict';

angular.module('sespaFilters', []).filter('colorToStatus', function () {
  return function (statusOutput) {
    if(statusOutput === 'green'){
      return 'Encourage';
    }
    else if(statusOutput === 'yellow') {
      return 'Explore';
    }
    else if(statusOutput === 'red') {
      return 'Engage';
    }
  };
});