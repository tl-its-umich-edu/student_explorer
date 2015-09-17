// For getting the data

(function(){
  'use strict';

  angular.module('students')
         .factory('StudentExplorerApiService', function($http,$q) {
         	var seapiService = {
	            students: function(student) { 
                    var promise = $http.get('api/advisors/burl/students/')
                                    .then(function(response) {
                        var data = []
                        response.data.results.forEach(function(entry) {
                            console.log(entry.student)
                            data.push(entry.student)
                        });
                        return data;
                    });
                    return promise;
	        	}
            };
          	return seapiService;
         });
})();
  
