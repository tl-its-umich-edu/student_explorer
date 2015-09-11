// For getting the data

(function(){
  'use strict';

  angular.module('students')
         .factory('StudentExplorerApiService', function($http,$q) {
         	var seapiService = {
	            students: function(student) { // Temporary provider of courses completed by currently logged in user
	              var students = [
	                {name: 'Fadia Ahmed', student_ID: 87654321, GPA: 1.9, year: 'Sophomore'},
	                {name: 'Max Black', student_ID: 87654322, GPA: 3.0, year: 'Freshman'},
	                {name: 'Xi Chiang', student_ID: 87654323, GPA: 3.6, year: 'Junior'},
	                {name: 'Maria Costolo', student_ID: 87654324, GPA: 2.5, year: 'Sophomore'},
	                {name: 'Martin Galvez', student_ID: 87654325, GPA: 2.4, year: 'Sophomore'}
	              ];        
	              return $q.when(students);
	        	}
            };
          	return seapiService;
         });
})();
  
