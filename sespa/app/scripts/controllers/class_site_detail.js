'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:ClassSiteDetailCtrl
 * @description
 * # ClassSiteDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('ClassSiteDetailCtrl', function(advisingData, advisingUtilities, $scope, $routeParams) {
    $scope.classSiteDetailHeader = null;
    $scope.assignments = null;
    $scope.classSiteHistory = null;
    $scope.historyLength = null;
    $scope.historyDate = null;
    $scope.classSiteDescription = null;
    $scope.sortTypeAssignment = 'assignment.due_date';
    $scope.sortTypeHistory = 'date';
    $scope.sortReverse = false;
    $scope.searchStudent = '';
    $scope.progress = 0;
    // $scope.scroll = scroll;



    advisingData.studentClassSiteDetails($routeParams.student, $routeParams.classSiteCode).then(function(classSite) {
      $scope.classSite = classSite;
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
      var event_count = [];
      for (var i = 0; i < classSiteHistory.length; i++) {
        studentData.push([classSiteHistory[i].week_number, classSiteHistory[i].score]);
        classData.push([classSiteHistory[i].week_number, classSiteHistory[i].class_score]);
        //add no data condition
        event_percentile.push([i + 1, classSiteHistory[i].event_percentile_rank * 100]);
      }


      $scope.scoreData = [{
        'key': 'Student %',
        'values': studentData,
        'bar': true,
        'color': '#255c91'
      }, {
        'key': 'Class %',
        'values': classData,
        'color': '#dac251'
      }];

      $scope.eventData = [{
        'key': 'Activity Percentile Rank',
        'values': event_percentile,
        'color': '#255c91'
      }];
    }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
    });

    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.student = student;
    }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
    });

    $scope.y1axislabeltext = 'Student %';
    $scope.y2axislabeltext = 'Class %';

    // nvd3 chart manipulation functions
    $scope.xAxisTickFormatFunction = function() {
      return function(d) {
        return '' + d;
      };
    };

    $scope.y1AxisTickFormat = function() {
      return function(d) {
        return d3.format(',f')(d);
      };
    };
    $scope.y2AxisTickFormat = function() {
      return function(d) {
        return '$' + d3.format(',.2f')(d);
      };
    };
    $scope.tooltipContentFunction = function() {
      return function(key, x, y, e, graph) {
        return '<p>' + y + '% in Week ' + x + '</p>';
      };
    };

  });
