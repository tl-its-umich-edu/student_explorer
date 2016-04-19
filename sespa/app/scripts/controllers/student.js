'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:StudentCtrl
 * @description
 * # StudentCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('StudentCtrl', function (advisingData, advisingUtilities, $scope, $routeParams, $location, $window) {
    $scope.studentUsername = $routeParams.student;
    $scope.student = null;
    $scope.advisors = null;
    $scope.mentors = null;
    $scope.classSites = null;
    $scope.sortTypeAdvisor = 'advisor.last_name';
    $scope.sortTypeMentor = 'mentor.last_name';
    $scope.sortType = 'class_site.description';
    $scope.sortReverseAdvisor = false;
    $scope.sortReverseMentor = false;
    $scope.sortReverse = false;
    $scope.classSiteDetailHeader = null;
    $scope.assignments = null;
    $scope.classSiteHistory = null;
    $scope.historyLength = null;
    $scope.historyDate = null;
    $scope.classSiteDescription = null;
    $scope.sortTypeAssignment = 'assignment.due_date';
    $scope.sortTypeHistory = 'week_end_date';
    $scope.searchStudent = '';
    $scope.progress = 0;
    $scope.showComment = false;
    $scope.goTo = function(loc) {
      $location.path(loc);
    };

    $scope.isStudentDetail = function() {
      var strings = $location.path().split('/');
      if (strings[3] === '') {
        return true;
      }
      return false;
    };

    $scope.isStudentClassSiteDetail = function() {
      var strings = $location.path().split('/');
      console.log(strings);
      if (strings[3] === 'class_sites') {
        return true;
      }
      return false;
    };

    if ($scope.studentUsername !== null && $scope.studentUsername !== undefined) {
      advisingData.studentDetails($scope.studentUsername).then(function(student) {
        $scope.student = student;
      }, function(reason) {
          advisingUtilities.httpErrorHandler(reason, $scope, true);
      });
    }

    if ($scope.studentUsername !== null && $scope.studentUsername !== undefined) {
      advisingData.studentAdvisors($scope.studentUsername).then(function(advisors) {
        $scope.advisors = advisors;
      }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
      });
    }

    if ($scope.studentUsername !== null && $scope.studentUsername !== undefined) {
      advisingData.studentClassSites($scope.studentUsername).then(function(class_sites) {
        $scope.classSites = class_sites;
      }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
      });
    }

    if ($routeParams.student !== null && $routeParams.student !== undefined && $routeParams.classSiteCode !== null && $routeParams.classSiteCode !== undefined) {
      advisingData.studentClassSiteDetails($routeParams.student, $routeParams.classSiteCode).then(function(classSite) {
        $scope.classSite = classSite;
      }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope, true);
      });
    }

    if ($routeParams.student !== null && $routeParams.student !== undefined && $routeParams.classSiteCode !== null && $routeParams.classSiteCode !== undefined) {
      advisingData.studentClassSiteAssignments($routeParams.student, $routeParams.classSiteCode).then(function(assignment) {
        $scope.progress = 100;
        $scope.assignments = assignment;
      }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
      }, function(update) {
        advisingUtilities.updateProgress(update, $scope);
      });
    }

    if ($routeParams.student !== null && $routeParams.student !== undefined && $routeParams.classSiteCode !== null && $routeParams.classSiteCode !== undefined) {
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
            return d > 0 ? Math.round(d) + '%ile' : '';
          };
        };
        $scope.xTickFormat = function() {
          return function(d) {
            if ($window.innerWidth >= 1150) {
              return d > 0 ? 'Week ' + d : '';
            }
            return d > 0 ? d : '';
          };
        };

      }, function(reason) {
        advisingUtilities.httpErrorHandler(reason, $scope);
      });
    }
  });

function toggleAssignment(element) {
  var code = element.id;
  if (!$('#collapse'+code).hasClass('collapsing')) {
    var sign = $(element).children().attr('src');
    $('[class="assignment-button"]').attr('src', 'images/Dropdown_Plus.png');
    $('#assignmentButton'+code).attr('src', (sign === 'images/Dropdown_Plus.png') ? 'images/Dropdown_Minus.png' : 'images/Dropdown_Plus.png');
  }
}
