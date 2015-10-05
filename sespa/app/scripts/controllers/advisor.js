'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:AdvisorCtrl
 * @description
 * # AdvisorCtrl
 * Controller of the sespaApp
 */

function AdvisorCtrl(StudentService) {
  var self = this;

  self.selected = null;
  self.advisors = [];
  self.sortType = 'last_name';
  self.sortReverse = false;
  self.searchAdvisor = '';
  self.scroll = scroll;

  //Get data for advisors' list
  StudentService
    .advisors()
    .then(function(advisor) {
      self.advisors = [].concat(advisor);
    });

  // function scroll() {
  //   window.scrollTo(0, 0);
  // }
}

angular
  .module('sespaApp')
  .controller('AdvisorCtrl', [
    'StudentService', '$log', '$q', '$scope', '$http',
    AdvisorCtrl
  ]);
