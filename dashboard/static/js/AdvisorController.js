(function(){

  angular
      .module('advisors')
      .controller('AdvisorController', [
           'StudentExplorerApiService', '$log', '$q', '$scope', '$http',
          AdvisorController
      ])
  ;

  /**
   * Advisor Controller for the Student Explorer App
   * @param StudentExplorerApiService
   * @param $log
   * @param $q
   * @param $scope
   * @constructor
   */
  function AdvisorController( StudentExplorerApiService, $log, $q, $scope, $http ) {
    var self = this;

    self.selected             = null;
    self.advisors             = [ ];
    self.sortType             = 'last_name';
    self.sortReverse          = false;
    self.searchAdvisor        = '';

    //Get data for advisors' list
    StudentExplorerApiService
          .advisors()
          .then(function(advisor) {
            self.advisors = [].concat(advisor);
          });
  }

})();
