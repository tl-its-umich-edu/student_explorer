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
    self.options              = null;

    StudentExplorerApiService
          .students()
          .then( function( student ) {
          self.students = [].concat(student);
          });

    self.options = {
      rowHeight: 50,
      headerHeight: 50,
      footerHeight: false,
      scrollbarV: false,
      selectable: false,
      columns: [{
        name: "Name",
        width: 300
      }, {
        name: "student_ID"
      }, {
        name: "GPA"
      }, {
        name: "year"
      }]
    };
    // *********************************
    // Internal methods
    // *********************************

  }

})();
