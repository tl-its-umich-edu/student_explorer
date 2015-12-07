'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:ClassSiteDetailCtrl
 * @description
 * # ClassSiteDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('ClassSiteDetailCtrl', function(advisingData, $scope, $routeParams) {
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
    // $scope.scroll = scroll;



    advisingData.studentClassSites($routeParams.student).then(function(class_sites) {
      class_sites.forEach(function(class_site) {
        if (class_site.class_site.code === $routeParams.classSiteCode) {
          $scope.classSiteDescription = class_site.class_site.description;
        }
      });
    });

    advisingData.studentClassSiteAssignments($routeParams.student, $routeParams.classSiteCode).then(function(assignment) {
      $scope.assignments = assignment;
    });

    advisingData.studentClassSiteHistory($routeParams.student, $routeParams.classSiteCode).then(function(classSiteHistory) {
      $scope.classSiteHistory = classSiteHistory;
      $scope.historyDate = Object.keys(classSiteHistory);
      $scope.historyLength = $scope.historyDate.length;
      var studentData = [];
      var classData = [];
      for (var i = 0; i < classSiteHistory.length; i++) {
        studentData.push([i + 1, classSiteHistory[i].score]);
        classData.push([i + 1, classSiteHistory[i].class_score]);
      }
      $scope.scoreData = [{
        'key': 'student',
        'values': studentData
      }, {
        'key': 'class',
        'values': classData
      }];
    });

    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.classSiteDetailHeader = student.first_name + ' ' + student.last_name;
    });

  });
