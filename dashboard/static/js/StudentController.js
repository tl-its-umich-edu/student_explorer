(function(){

  angular
      .module('students')
      .controller('StudentController', [
           'StudentExplorerApiService', '$log', '$q', '$scope', '$mdUtil',
          StudentController
      ])
  ;

  /**
   * Main Controller for the SE App
   * @param SEApiService
   * @param $mdSidenav
   * @param $mdBottomSheet
   * @param $log
   * @param $q
   * @param $scope
   * @param $mdUtil
   * @param $timeout
   * @constructor
   */
  function StudentController( StudentExplorerApiService, $log, $q, $scope, $mdUtil ) {
    var self = this;

    self.selected             = null;
    self.students             = [ ];
    self.sortType             = 'name';
    self.sortReverse          = false;
    self.searchStudent        = '';
    self.checkGPA             = checkGPA;
    self.checkYear            = checkYear;
    self.icons                = [];

    self.gpaSlider            = { min:0, max:4};
    self.classStanding        = { Freshman: true, Sophomore: true, Junior: true, Senior: true};

    StudentExplorerApiService
          .students()
          .then( function( student ) {
          self.students = [].concat(student);
          });

    self.icons = [
      {name:"Engage", url:'{{STATIC_URL}}images/Status_Icons_Engage.png'},
      {name:"Explore", url:'{{STATIC_URL}}images/Status_Icons_Explore.png'},
      {name:"Encourage", url:'{{STATIC_URL}}images/Status_Icons_Encourage.png'}
    ]

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
