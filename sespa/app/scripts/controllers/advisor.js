'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:AdvisorcontrollerCtrl
 * @description
 * # AdvisorcontrollerCtrl
 * Controller of the sespaApp
 */
angular
      .module('sespaApp')
      .controller('AdvisorcontrollerCtrl', [
           'StudentService', '$log', '$q', '$scope', '$http',
          AdvisorcontrollerCtrl
      ])
  ;

function AdvisorcontrollerCtrl( StudentService, $log, $q, $scope, $http ) {
  var self = this;

  self.selected             = null;
  self.advisors             = [ ];
  self.sortType             = 'last_name';
  self.sortReverse          = false;
  self.searchAdvisor        = '';
  self.scroll               = scroll;

  //Get data for advisors' list
  StudentService
        .advisors()
        .then(function(advisor) {
          self.advisors = [].concat(advisor);
        });

  function scroll() {
    window.scrollTo(0,0);
  }
}