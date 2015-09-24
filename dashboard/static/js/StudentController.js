(function(){

  angular
      .module('students')
      .controller('StudentController', [
           'StudentExplorerApiService', '$log', '$q', '$scope', '$http',
          StudentController
      ])
  ;

  /**
   * Main Controller for the Student Explorer App
   * @param StudentExplorerApiService
   * @param $log
   * @param $q
   * @param $scope
   * @constructor
   */
  function StudentController( StudentExplorerApiService, $log, $q, $scope, $http ) {
    var self = this;

    self.selected             = null;
    self.students             = [ ];
    self.selectedStudent      = window.location.pathname.replace(/\//g,"").replace("student","");
    self.sortType             = 'last_name';
    self.sortReverse          = false;
    self.searchStudent        = '';

    self.icons = [
      {name:"Engage", url:static_url+'images/Status_Icons_Engage.png', color:"Red"},
      {name:"Explore", url:static_url+'images/Status_Icons_Explore.png', color:"Yellow"},
      {name:"Encourage", url:static_url+'images/Status_Icons_Encourage.png', color:"Green"}
    ];

    self.additionalIcons = [
      {name:"Student Grade", url:static_url+'images/Status_Icons_Student.png'},
      {name:"Class Average", url:static_url+'images/Status_Icons_ClassAverage.png'}
    ];

    //Filter variables
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

    StudentExplorerApiService
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

    StudentExplorerApiService
          .student(self.selectedStudent)
          .then(function(d) {
            promise = [].concat(d);
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

    // Filters
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
  }

})();
