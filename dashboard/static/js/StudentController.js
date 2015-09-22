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
    self.advisor              = null;
    self.students             = [ ];
    self.selectedStudent      = '';
    self.sortType             = 'last_name';
    self.sortReverse          = false;
    self.searchStudent        = '';
    self.checkStatus          = checkStatus;
    self.checkGPA             = checkGPA;
    self.checkYear            = checkYear;
    self.icons                = [ ];

    self.gpaSlider            = { min:0, max:4};
    self.classStanding        = { Freshman: true, Sophomore: true, Junior: true, Senior: true };
    self.statusType           = { Engage: true, Explore: true, Encourage: true };

    StudentExplorerApiService
          .students()
          .then(function(student) {
            self.students = [].concat(student);
          });

    StudentExplorerApiService
          // .student(self.selectedStudent)
          .student('graciela')
          .then(function(d) {
            promise = [].concat(d);
            self.selected = promise[0];
            getAdvisor();
          });

    function getAdvisor() {
      StudentExplorerApiService
            .advisor(self.selected.advisors_url)
            .then(function(d) {
              promise = [].concat(d);
              self.advisor = promise[0].results[0].advisor;
            });
    }

    self.icons = [
      {name:"Engage", url:static_url+'images/Status_Icons_Engage.png'},
      {name:"Explore", url:static_url+'images/Status_Icons_Explore.png'},
      {name:"Encourage", url:static_url+'images/Status_Icons_Encourage.png'}
    ];

    self.additionalIcons = [
      {name:"Student Grade", url:static_url+'images/Status_Icons_Student.png'},
      {name:"Class Average", url:static_url+'images/Status_Icons_ClassAverage.png'}
    ];

    function checkStatus(stat) {
      return self.statusType[stat];
    }

    function checkGPA(GPA) {
      if (GPA >= self.gpaSlider.min && GPA <= self.gpaSlider.max) {
        return true;
      }
      return false;
    }

    function checkYear(year) {
      return self.classStanding[year];
    }
  }

})();
