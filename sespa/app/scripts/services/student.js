'use strict';

/**
 * @ngdoc service
 * @name sespaApp.StudentService
 * @description
 * # StudentService
 * Factory in the sespaApp.
 */

function getData(url, data, $http) {
  $http.get(url).then(function(response) {
    response.data.results.forEach(function(entry) {
      data.push(entry);
    });
    if (response.data.next !== null) {
      getData(response.data.next, data, $http);
    }
  });
  console.log(data);
  return data;
}

angular.module('sespaApp')
  .factory('StudentService', function($http) {
    var seapiService = {
      students: function() {
        var data = [];
        $http.get('http://localhost:2080/api/students/')
          .then(function(response) {
            response.data.results.forEach(function(entry) {
              // console.log(entry)
              // entry.status = [{engage: Math.floor(Math.random()*5), explore: Math.floor(Math.random()*5), encourage: Math.floor(Math.random()*5)}]
              // entry.GPA = (Math.random()*4).toFixed(1)
              // entry.year = selectYear()
              data.push(entry);
            });
            if (response.data.next !== null) {
              getData(response.data.next, data, $http);
            }
            console.log(data);
            return data;
          });
        return data;
      },
      student: function(student) {
        var promise = $http.get('http://localhost:2080/api/students/' + student + '/full/')
          .then(function(response) {
            return response.data;
          });
        return promise;
      },
      advisors: function() {
        var promise = $http.get('http://localhost:2080/api/advisors/')
          .then(function(response) {
            var data = [];
            response.data.results.forEach(function(entry) {
              // console.log(entry)
              data.push(entry);
            });
            // console.log(data);
            return data;
          });
        return promise;
      },
      advisor: function(advisor) {
        var promise = $http.get('http://localhost:2080/api/advisors/' + advisor + '/')
          .then(function(response) {
            return response.data;
          });
        return promise;
      }
    };
    return seapiService;
  });

// function selectYear() {
//   var num = Math.floor(Math.random() * 4);
//   if (num === 0) {
//     return 'Freshman';
//   } else if (num === 1) {
//     return 'Sophomore';
//   } else if (num === 2) {
//     return 'Junior';
//   } else if (num === 3) {
//     return 'Senior';
//   } else {
//     return selectYear();
//   }
// }
