'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:AdvisorCtrl
 * @description
 * # AdvisorCtrl
 * Controller of the sespaApp
 */

angular
  .module('sespaApp')
  .controller('AdvisorCtrl', function(studentExplorer) {
    this.selected = null;
    this.sortType = 'last_name';
    this.sortReverse = false;
    this.searchAdvisor = '';
    this.scroll = scroll;

    this.advisors = [];
    studentExplorer.addAllAdvisors(this.advisors);
  });
