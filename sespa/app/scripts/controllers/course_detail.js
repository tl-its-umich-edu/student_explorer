'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:CourseDetailCtrl
 * @description
 * # CourseDetailCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('CourseDetailCtrl', function(advisingData, $scope, $routeParams) {
    $scope.courseDetailHeader = null;
    $scope.courseDescription = $routeParams.course;
    $scope.sortType = 'last_name';
    $scope.sortReverse = false;
    $scope.searchStudent = '';
    // $scope.scroll = scroll;

    $scope.assignments = [];

    advisingData.studentCourseAssignments($routeParams.student, $routeParams.courseCode).then(function(assignment) {
      $scope.assignments = assignment;
    });
    
    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.courseDetailHeader = student.first_name + ' ' + student.last_name;
    });
    
  });
