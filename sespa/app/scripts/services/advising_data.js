'use strict';

/**
 * @ngdoc service
 * @name sespaApp.advisingService
 * @description
 * # advisingService
 * Factory in the sespaApp.
 */
angular.module('sespaApp')
  .factory('advisingData', function($http) {
    var config = {
      _conf: {
        'students': 'http://localhost:2080/api/students/',
        'username': '',
        'advisors': 'http://localhost:2080/api/advisors/',
        'debug': true
      },
      get: function(item) {
        return this._conf[item];
      },

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
      allAdvisors: function() {
        var promise = $http.get(config.get('advisors'))
          .then(function(response) {
            return response.data;
          });
        return promise;
      },

      allStudents: function() {
        var promise = $http.get(config.get('students'))
          .then(function(response) {
            return response.data;
          });
        return promise;
      }

    };
  });
