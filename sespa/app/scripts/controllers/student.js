'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:StudentCtrl
 * @description
 * # StudentCtrl
 * Controller of the sespaApp
 */
angular
    .module('sespaApp')
    .controller('StudentCtrl', [
         'StudentService', '$log', '$q', '$scope', '$http', '$routeParams',
        StudentCtrl
    ])
;

function StudentCtrl( StudentService, $log, $q, $scope, $http, $routeParams ) {
  var self = this;

  self.selected             = null;
  self.students             = [ ];
  self.selectedStudent      = $routeParams.student;
  self.selectedAdvisorName  = $routeParams.advisor;
  self.selectedAdvisor      = [ ];
  self.sortType             = 'last_name';
  self.sortReverse          = false;
  self.searchStudent        = '';
  self.goToDashboard        = goToDashboard;
  self.goToAdvisorDashboard = goToAdvisorDashboard;
  self.scroll               = scroll;

  self.icons = [
    {name:"Engage", url:'images/Status_Icons_Engage.png', color:"Red"},
    {name:"Explore", url:'images/Status_Icons_Explore.png', color:"Yellow"},
    {name:"Encourage", url:'images/Status_Icons_Encourage.png', color:"Green"}
  ];

  self.additionalIcons = [
    {name:"Student Grade", url:'images/Status_Icons_Student.png'},
    {name:"Class Average", url:'images/Status_Icons_ClassAverage.png'}
  ];

  //Filter variables
  self.checkAdvisor         = checkAdvisor;
  self.checkStatus          = checkStatus;
  self.checkGPA             = checkGPA;
  self.checkYear            = checkYear;

  self.hasStatusData        = false;
  self.hasGPAData           = false;
  self.hasYearData          = false;

  self.hasStudentStanding   = false;
  self.hasStudentGrade      = false;
  self.hasClassAverage      = false;

  self.gpaSlider            = { min:0, max:4};
  self.classStanding        = { Freshman: true, Sophomore: true, Junior: true, Senior: true };
  self.statusType           = { Engage: true, Explore: true, Encourage: true };

  //Get data for students' list
  StudentService
        .students()
        .then(function(student) {
          self.students = [].concat(student);
          //Filters
          for (var i=0;i<student.length;i++) {
            if (student[i].statuses != null) {
              self.hasStatusData = true;
            }
            if (student[i].GPA != null) {
              self.hasGPAData = true;
            }
            if (student[i].year != null) {
              self.hasYearData = true;
            }
            if (self.hasStatusData == true && self.hasGPAData == true && self.hasYearData == true) {
              break;
            }
          }
        });

  //Get data for selected student
  if (self.selectedStudent != null) {
	  StudentService
	          .student(self.selectedStudent)
	          .then(function(d) {
	            var promise = [].concat(d);
	            self.selected = promise[0];
	            //Filters
	            for (var i=0;i<self.selected.class_sites.length;i++) {
	              if (self.selected.class_sites[i].student_grade != null) {
	                self.hasStudentGrade = true;
	              }
	              if (self.selected.class_sites[i].class_average != null) {
	                self.hasClassAverage = true;
	              }
	              if (self.hasStudentGrade == true && self.hasClassAverage == true) {
	                self.hasStudentStanding = true;
	                break;
	              }
	            }
	          });
  }

  //Get data for advisor
  if (self.selectedAdvisorName != null) {
	  StudentService
	        .advisor(self.selectedAdvisorName)
	        .then(function(advisor) {
	          var promise = [].concat(advisor);
	          self.selectedAdvisor = promise[0];
	        });
  }

  // Filters
  function checkAdvisor(advisor) {
  	for (var i=0;i<advisor.length;i++) {
	    if (self.selectedAdvisorName != null && advisor[i] == self.selectedAdvisorName) {
	      return true;
	    }
	}
	return false;
  }

  function checkStatus(stat) {
    if (stat == null) {
      return true;
    }
    return self.statusType[stat];
  }

  function checkGPA(GPA) {
    if (GPA == null) {
      return true;
    }
    if (GPA >= self.gpaSlider.min && GPA <= self.gpaSlider.max) {
      return true;
    }
    return false;
  }

  function checkYear(year) {
    if (year == null) {
      return true;
    }
    return self.classStanding[year];
  }

  function scroll() {
    window.scrollTo(0,0);
  }

  function goToDashboard(advisor_username) {
  	console.log(advisor_username);
  	window.scrollTo(0, 0);
    window.location.href = "http://localhost:2080/#/"+advisor_username+"/studentList/";
  }

  function goToAdvisorDashboard(advisor_username) {
  	window.scrollTo(0, 0);
    window.location.href = "http://localhost:2080/#/advisorList";
  }
}
