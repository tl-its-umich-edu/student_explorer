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
      // }, {
      //   'key': 'Activity Percentile Rank',
      //   'values': event_percentile,
      //   'color': '#babdba',
      //   'disabled': true,
      }];

      var chart = nv.models.multiBarChart()
        .margin({
          left: 50,
          right: 50
        }) //Adjust chart margins to give the x-axis some breathing room.
        .transitionDuration(100) //how fast do you want the lines to transition?
        .showLegend(true) //Show the legend, allowing users to turn on/off line series.
        .showYAxis(true) //Show the y-axis
        .showXAxis(true) //Show the x-axis
        .showControls(false)
        .forceY([0, 100])
        .reduceXTicks(false)
        .groupSpacing(0.3)
      ;

      chart.yAxis
        .tickFormat(function(d) {
          if (d>0) {
            return d + '%'
          }
        })
      chart.xAxis //Chart x-axis settings
        .tickFormat(function(d) {
          return d > 0 ? 'Week ' + d : '';
        })
        .tickValues(weeks);

      d3.select('#chart svg') //Select the <svg> element you want to render the chart in.
        .datum($scope.scoreData) //Populate the <svg> element with chart data...
        .call(chart); //Finally, render the chart!

      //Update the chart when window resizes.
      nv.utils.windowResize(function() {
        chart.update()
      });
    }, function(reason) {
      advisingUtilities.httpErrorHandler(reason, $scope);
    });

    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.student = student;
    }, function(reason) {
      advisingUtilities.httpErrorHandler(reason, $scope);
    });
  });
