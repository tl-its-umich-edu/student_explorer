'use strict';

/**
 * @ngdoc service
 * @name sespaApp.advisingService
 * @description
 * # advisingService
 * Factory in the sespaApp.
 */
angular.module('sespaApp')
  .factory('advisingData', function($http, $q) {
    var config = function() {
      return $http.get('api/', {
          'cache': true
        })
        .then(function(response) {
          return response.data;
        });
    };

    var getAdvisingData = function(url) {
      var deferred = $q.defer();
      var data = [];
      var getNext = function(url) {
        console.log(url);
        
        $http.get(url).then(function(response) {
          response.data.results.forEach(function(entry) {
            data.push(entry);
          });

          if (response.data.next !== null) {
            getNext(response.data.next);
            // TODO deferred.notify()
          } else {
            deferred.resolve(data);
          }
        });
      };
      
      config().then(function(config) {
        getNext(config.apiRootUrl + url);
      });

      return deferred.promise;
    };

    // Public API here
    return {
      config: function() {
        return config();
      },

      userInfo: function() {
        return config().then(function() {
          return $http.get('api/users/me/', {
              'cache': true
            })
            .then(function(response) {
              return response.data;
            });
        });
      },

      allAdvisors: function() {
        return getAdvisingData('advisors/');
      },

      advisorDetails: function(advisorUsername) {
        return config().then(function(config) {
          if (typeof advisorUsername === 'undefined') {
            if (config.username !== null) {
              advisorUsername = config.username;
            } else {
              return null;
            }
          }
          return $http.get('api/advisors/' + advisorUsername + '/', {
              'cache': true
            })
            .then(function(response) {
              return response.data;
            });
        });
      },

      advisorsStudents: function(advisorUsername) {
        if (typeof advisorUsername === 'undefined') {
          if (config.username !== null) {
            advisorUsername = config.username;
          } else {
            return null;
          }
        }
        return $http.get('api/advisors/' + advisorUsername + '/students/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
      },

      searchStudents: function(search) {
        return $http.get('api/students/', {
            'params': {
              'search': search
            },
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
      },

      studentDetails: function(studentUsername) {
        return $http.get('api/students/' + studentUsername + '/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
      },

      studentAdvisors: function(studentUsername) {
        return $http.get('api/students/' + studentUsername + '/advisors/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
      },

      studentMentors: function(studentUsername) {
        return $http.get('api/students/' + studentUsername + '/mentors/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
      },

      studentClassSites: function(studentUsername) {
        return $http.get('api/students/' + studentUsername + '/class_sites/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
      },

      studentClassSiteAssignments: function(studentUsername, classSiteCode) {
        return $http.get('api/students/' + studentUsername + '/class_sites/' + classSiteCode + '/assignments/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
      },

      studentClassSiteHistory: function(studentUsername, classSiteCode) {
        return $http.get('api/students/' + studentUsername + '/class_sites/' + classSiteCode + '/history/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
      },

    };
  });
