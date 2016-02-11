'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:ClassSiteDetailCtrl
 * @description
 * # ClassSiteDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('StudentClassSiteDetailCtrl', function(advisingData, advisingUtilities, $scope, $routeParams) {
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
      var weeks = [];
      for (var i = 0; i < classSiteHistory.length; i++) {
        weeks.push(i + 1);
        studentData.push({
          x: classSiteHistory[i].week_number,
          y: classSiteHistory[i].score
        });
        classData.push({
          x: classSiteHistory[i].week_number,
          y: classSiteHistory[i].class_score
        });
        event_percentile.push({
          x: i + 1,
          y: classSiteHistory[i].event_percentile_rank * 100
        });
      }

      $scope.scoreData = [{
        'key': 'Student',
        'values': studentData,
        'color': '#255c91'
      }, {
        'key': 'Class',
        'values': classData,
        'color': '#dac251',
      }];

      $scope.activityData = [{
        'key': 'Course Site Engagement',
        'values': event_percentile,
        'color': '#a9bdab',
        // 'disabled': true,
      }];

      var scoreChart = nv.models.multiBarChart()
        .margin({
          left: 50,
          right: 50
        })
        .transitionDuration(100)
        .showLegend(true)
        .showYAxis(true)
        .showXAxis(true)
        .showControls(false)
        .forceY([0, 100])
        .reduceXTicks(false)
        .groupSpacing(0.3);
        scoreChart.yAxis.tickFormat(function(d) {
          if (d>0) {
            return d + '%'
          }
        })
        scoreChart.xAxis.tickFormat(function(d) {
          return d > 0 ? 'Week ' + d : '';
        })
        .tickValues(weeks);

      d3.select('#assignments-chart svg')
        .datum($scope.scoreData)
        .call(scoreChart);

      var activityChart = nv.models.multiBarChart()
        .margin({
          left: 50,
          right: 50
        })
        .transitionDuration(100)
        .showLegend(true)
        .showYAxis(true)
        .showXAxis(true)
        .showControls(false)
        .forceY([0, 100])
        .reduceXTicks(false)
        .groupSpacing(0.3);
        activityChart.yAxis.tickFormat(function(d) {
          if (d>0) {
            return d + '%ile'
          }
        })
        activityChart.xAxis.tickFormat(function(d) {
          return d > 0 ? 'Week ' + d : '';
        })
        .tickValues(weeks);

      d3.select('#activity-chart svg')
        .datum($scope.activityData)
        .call(activityChart);

    }, function(reason) {
      advisingUtilities.httpErrorHandler(reason, $scope);
    });

    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.student = student;
    }, function(reason) {
      advisingUtilities.httpErrorHandler(reason, $scope);
    });
  });
