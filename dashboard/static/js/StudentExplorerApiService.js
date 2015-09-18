// For getting the data

(function(){
  'use strict';

  angular.module('students')
         .factory('StudentExplorerApiService', function($http,$q) {
         	var seapiService = {
	            students: function(student) { 
                    var promise = $http.get('api/students/')
                                    .then(function(response) {
                        var data = []
                        response.data.results.forEach(function(entry) {
                            console.log(entry)
                            // entry.status = [{engage: Math.floor(Math.random()*5), explore: Math.floor(Math.random()*5), encourage: Math.floor(Math.random()*5)}]
                            entry.GPA = (Math.random()*4).toFixed(1)
                            entry.year = selectYear()
                            data.push(entry)
                        });
                        console.log(data);
                        return data;
                    });
                    return promise;
	        	}
            };
          	return seapiService;
         });

    function selectYear(){
    	var num = Math.floor(Math.random()*4);
    	if (num == 0) {
    		return "Freshman";
    	} else if (num == 1) {
    		return "Sophomore";
    	} else if (num == 2) {
    		return "Junior";
    	} else if (num == 3) {
    		return "Senior";
    	} else {
    		return selectYear();
    	}
    }
})();
  
