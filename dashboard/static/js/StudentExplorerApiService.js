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
                            entry.student.status = [{engage: Math.floor(Math.random()*5), explore: Math.floor(Math.random()*5), encourage: Math.floor(Math.random()*5)}]
                            entry.student.GPA = (Math.random()*4).toFixed(1)
                            entry.student.year = selectYear()
                            data.push(entry.student)
                        });
                        return data;
                    });
                    return promise;
	        	},
	        	student: function(student) {
	        		var data = $http.get('api/students/'+student+'/')
	        						.then(function(response) {
	        							return data;
	        						})
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
  
