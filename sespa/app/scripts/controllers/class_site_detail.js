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
    $scope.sortTypeAssignment = 'assignment.description';
    $scope.sortTypeHistory = 'date';
    $scope.sortReverse = false;
    $scope.searchStudent = '';
    $scope.progress = 0;
    // $scope.scroll = scroll;



    advisingData.studentClassSites($routeParams.student).then(function(class_sites) {
      class_sites.forEach(function(class_site) {
        if (class_site.class_site.code === $routeParams.classSiteCode) {
          $scope.classSiteDescription = class_site.class_site.description;
        }
      });
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
      for (var i = 0; i < classSiteHistory.length; i++) {
        studentData.push([i + 1, classSiteHistory[i].score]);
        classData.push([i + 1 , classSiteHistory[i].class_score]);
      }
      $scope.scoreData = [{
        'key': 'Student',
        'values': studentData
      }, {
        'key': 'Class',
        'values': classData
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
