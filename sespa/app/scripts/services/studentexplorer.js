'use strict';

/**
 * @ngdoc service
 * @name sespaApp.studentExplorer
 * @description
 * # studentExplorer
 * Factory in the sespaApp.
 */
angular.module('sespaApp')
  .factory('studentExplorer', function($http) {
    var config = {
      'students': 'http://localhost:2080/api/students/',
      'username': '',
      'advisors': 'http://localhost:2080/api/advisors/',
      'debug': true
    };

    var pushPaginatedData = function(obj, url) {
      $http.get(url).then(function(response) {
        response.data.results.forEach(function(entry) {
          obj.push(entry);
        });
        console.log(obj, response.data.next, response);

        if (response.data.next !== null) {
          pushPaginatedData(obj, response.data.next);
        }
      });
    };

    // Public API here
    return {
      addAllAdvisors: function(obj) {
        pushPaginatedData(obj, config.advisors);
      }
    };
  });
