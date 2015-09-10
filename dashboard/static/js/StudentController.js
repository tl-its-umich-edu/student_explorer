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

    StudentExplorerApiService
          .students()
          .then( function( student ) {
          self.students = [].concat(student);
          });

    // *********************************
    // Internal methods
    // *********************************

  }

})();
