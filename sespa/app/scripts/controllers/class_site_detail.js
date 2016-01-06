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
      window.alert(reason);
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
        studentData.push([i + 1, classSiteHistory[i].score]);
        classData.push([i + 1 , classSiteHistory[i].class_score]);
        //add no data condition
        event_percentile.push([i+1,classSiteHistory[i].event_percentile_rank*100]);
      }
      
      $scope.scoreData = [{
        'key': 'Student',
        'values': studentData
      }, {
        'key': 'Class',
        'values': classData
      }];
      
      $scope.eventData = [{
        'key': 'Percentile',
        'values': event_percentile
      }];
    });

    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.classSiteDetailHeader = student.first_name + ' ' + student.last_name;
    });
    
    // nvd3 chart manipulation functions
    $scope.xAxisTickFormatFunction = function(){
      return function(d){
        return 'Week  ' + d;
      };
    }

  });
