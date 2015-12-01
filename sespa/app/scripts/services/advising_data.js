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
        $http.get(url).then(function(response) {
          if ((typeof response.data.results === 'object' &&
              (typeof response.data.next === 'string' ||
                response.data.next === null)
            )) {
            // console.log('dealing with paginaged data');
            response.data.results.forEach(function(entry) {
              data.push(entry);
            });

            if (typeof response.data.count === 'number') {
              deferred.notify(data.length / response.data.count);
            }

            if (response.data.next !== null) {
              getNext(response.data.next);
            } else {
              deferred.resolve(data);
            }
          } else {
            // console.log('dealing with unpaginaged data');
            deferred.resolve(response.data);
          }
        }, function(reason) {
          deferred.reject('Failed to load data (' + url + ' ' + reason.status + ')');
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
        return getAdvisingData('users/me/');
      },

      allAdvisors: function() {
        return getAdvisingData('advisors/');
      },

      advisorDetails: function(advisorUsername) {
        return getAdvisingData('advisors/' + advisorUsername + '/');
      },

      advisorsStudents: function(advisorUsername) {
        return getAdvisingData('advisors/' + advisorUsername + '/students/');
      },

      searchStudents: function(search) {
        return getAdvisingData('students/?search=' + search);
      },

      studentDetails: function(studentUsername) {
        return getAdvisingData('students/' + studentUsername + '/');
      },

      studentAdvisors: function(studentUsername) {
        return getAdvisingData('students/' + studentUsername + '/advisors/');
      },

      studentMentors: function(studentUsername) {
        return getAdvisingData('students/' + studentUsername + '/mentors/');
      },

      studentClassSites: function(studentUsername) {
        return getAdvisingData('students/' + studentUsername + '/class_sites/');
      },

      studentClassSiteAssignments: function(studentUsername, classSiteCode) {
        return getAdvisingData('students/' + studentUsername + '/class_sites/' + classSiteCode + '/assignments/');
      },

      studentClassSiteHistory: function(studentUsername, classSiteCode) {
        return getAdvisingData('students/' + studentUsername + '/class_sites/' + classSiteCode + '/history/');
      },

    };
  });
