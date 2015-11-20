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
    var config = function() {
      return $http.get('api/', {'cache': true})
        .then(function(response) {
          return response.data;
        });
    };

    var pushPaginatedData = function(obj, url) {
      $http.get(url).then(function(response) {
        response.data.results.forEach(function(entry) {
          obj.push(entry);
        });

        if (response.data.next !== null) {
          pushPaginatedData(obj, response.data.next);
        }
      });
    };

    // Public API here
    return {
      config: function() {
        return config();
      },
      
      userInfo: function() {
        return config().then(function() {
          return $http.get('api/users/me/', {'cache': true})
            .then(function(response) {
              return response.data;
            });
        });
      },

      allAdvisors: function() {
        return config().then(function(config) {
          return $http.get(config.advisors, {
              'cache': true
            })
            .then(function(response) {
              return response.data;
            });
        });
      },

      advisorDetails: function(advisorUsername) {
        return config().then(function(config) {
          if (typeof advisorUsername === 'undefined') {
            if (config.username !== null){
              advisorUsername = config.username;
            } else {
              return null;
            }
          }
          return $http.get(config.advisors + advisorUsername + '/', {
              'cache': true
            })
            .then(function(response) {
              return response.data;
            });
        });
      },

      advisorsStudents: function(advisorUsername) {
        return config().then(function(config) {
          if (typeof advisorUsername === 'undefined') {
            if (config.username !== null){
              advisorUsername = config.username;
            } else {
              return null;
            }
          }
          return $http.get(config.advisors + advisorUsername + '/students/', {
              'cache': true
            })
            .then(function(response) {
              return response.data;
            });
        });
      },

      searchStudents: function(search) {
        return config().then(function(config) {
          return $http.get(config.students, {
              'params': {'search': search},
              'cache': true
            })
            .then(function(response) {
              return response.data;
            });
        });
      },

      studentDetails: function(studentUsername) {
        return config().then(function(config) {
          return $http.get(config.students + studentUsername + '/', {
              'cache': true
            })
            .then(function(response) {
              return response.data;
            });
        });
      },
      
      studentAdvisors: function(studentUsername) {
        return config().then(function(config) {
          return $http.get(config.students + studentUsername + '/advisors/', {
              'cache': true
            })
            .then(function(response) {
              return response.data;
            });
        });
      },
      
      studentMentors: function(studentUsername) {
        return config().then(function(config) {
          return $http.get(config.students + studentUsername + '/mentors/', {
              'cache': true
            })
            .then(function(response) {
              return response.data;
            });
        });
      },
      
      studentClassSites: function(studentUsername) {
        return config().then(function(config) {
          return $http.get(config.students + studentUsername + '/class_sites/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
        });
      },
      
      studentClassSiteAssignments: function(studentUsername, classSiteCode) {
        return config().then(function(config) {
          return $http.get(config.students + studentUsername + '/class_sites/' + classSiteCode + '/assignments/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
        });
      },
      
      studentClassSiteHistory: function(studentUsername, classSiteCode) {
        return config().then(function(config) {
          return $http.get(config.students + studentUsername + '/class_sites/' + classSiteCode + '/history/', {
            'cache': true
          })
          .then(function(response) {
            return response.data;
          });
        });
      },

    };
  });
