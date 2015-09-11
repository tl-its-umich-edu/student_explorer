// For getting the data

(function(){
  'use strict';

  angular.module('students')
         .factory('StudentExplorerApiService', function($http,$q) {
         	var seapiService = {
	            students: function(student) { // Temporary provider of courses completed by currently logged in user
	              var students = [
	                {name: 'Fadia Ahmed', student_ID: 87654321, status:[{engage:4, explore:1, encourage:0}], cohorts:[{cohorts_name:'Special Probation'},{cohorts_name:'CSP Summer Bridge'}], GPA: 1.9, year: 'Sophomore'},
	                {name: 'Max Black', student_ID: 87654322, status:[{engage:0, explore:0, encourage:4}], cohorts:[{cohorts_name:'CSP General'}], GPA: 3.0, year: 'Freshman'},
	                {name: 'Xi Chiang', student_ID: 87654323, status:[{engage:0, explore:2, encourage:3}], cohorts:[{cohorts_name:'CSP Winter'}], GPA: 3.6, year: 'Junior'},
	                {name: 'Maria Costolo', student_ID: 87654324, status:[{engage:3, explore:1, encourage:1}], cohorts:[{cohorts_name:'MSCI Fall'}], GPA: 2.5, year: 'Sophomore'},
	                {name: 'Martin Galvez', student_ID: 87654325, status:[{engage:0, explore:1, encourage:3}], cohorts:[{cohorts_name:'Special Probation'},{cohorts_name:'Athletics'}], GPA: 2.4, year: 'Sophomore'}
	              ];        
	              return $q.when(students);
	        	}
            };
          	return seapiService;
         });
})();
  
