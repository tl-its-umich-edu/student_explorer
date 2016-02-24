'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:ClassSiteDetailCtrl
 * @description
 * # ClassSiteDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('StudentClassSiteDetailCtrl', function(advisingData, advisingUtilities, $scope, $routeParams, $window) {
    $scope.classSiteDetailHeader = null;
    $scope.assignments = null;
    $scope.classSiteHistory = null;
    $scope.historyLength = null;
    $scope.historyDate = null;
    $scope.classSiteDescription = null;
    $scope.sortTypeAssignment = 'assignment.due_date';
    $scope.sortTypeHistory = 'week_end_date';
    $scope.sortReverse = false;
    $scope.searchStudent = '';
    $scope.progress = 0;
    $scope.windowWidth = window.innerWidth;
    // $scope.scroll = scroll;



    advisingData.studentClassSiteDetails($routeParams.student, $routeParams.classSiteCode).then(function(classSite) {
      $scope.classSite = classSite;
    }, function(reason) {
      advisingUtilities.httpErrorHandler(reason, $scope, true);
    });

    advisingData.studentClassSiteAssignments($routeParams.student, $routeParams.classSiteCode).then(function(assignment) {
      $scope.progress = 100;
      $scope.assignments = assignment;
    }, function(reason) {
      advisingUtilities.httpErrorHandler(reason, $scope);
    }, function(update) {
      advisingUtilities.updateProgress(update, $scope);
    });

    advisingData.studentClassSiteHistory($routeParams.student, $routeParams.classSiteCode).then(function(classSiteHistory) {
      $scope.classSiteHistory = classSiteHistory;
      $scope.historyDate = Object.keys(classSiteHistory);
      $scope.historyLength = $scope.historyDate.length;
      var studentData = [];
      var classData = [];
      var event_percentile = [];
      for (var i = 0; i < classSiteHistory.length; i++) {
        studentData.push([
          classSiteHistory[i].week_number,
          classSiteHistory[i].score
        ]);
        classData.push([
          classSiteHistory[i].week_number,
          classSiteHistory[i].class_score
        ]);
        event_percentile.push([
          i + 1,
          classSiteHistory[i].event_percentile_rank * 100
        ]);
      }

      $scope.scoreData = [{
        'key': 'Student',
        'values': studentData,
        'color': '#255c91'
      }, {
        'key': 'Class',
        'values': classData,
        'color': '#F0D654',
      }];

      $scope.activityData = [{
        'key': 'Course Site Engagement',
        'values': event_percentile,
        'color': '#a9bdab',
      }];

      $scope.scoreYTickFormat = function() {
        return function(d) {
          return d > 0 ? d + '%' : '';
        };
      };
      $scope.activityYTickFormat = function() {
        return function(d) {
          return d > 0 ? d + '%ile' : '';
        };
      };
      $scope.xTickFormat = function() {
        return function(d) {
          return d > 0 ? 'Week ' + d : '';
        };
      };

    }, function(reason) {
      advisingUtilities.httpErrorHandler(reason, $scope);
    });

    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.student = student;
    }, function(reason) {
      advisingUtilities.httpErrorHandler(reason, $scope);
    });
    
    $scope.$watch(function() {
        $scope.windowWidth = window.innerWidth;
    });
    
    angular.element($window).bind('resize', function() {
      $scope.$apply();
    });
    
    $scope.changeButton = function(code) {
      if (!$('#collapse'+code).hasClass('collapsing')) {
        var sign = $('#assignmentButton'+code).attr('src');
        $('[class="assignment-button"]').attr('src', 'images/Dropdown_Plus.png');
        $('#assignmentButton'+code).attr('src', (sign === 'images/Dropdown_Plus.png') ? 'images/Dropdown_Minus.png' : 'images/Dropdown_Plus.png');
      }
    };
  });
