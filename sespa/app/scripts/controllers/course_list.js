'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:CourseListCtrl
 * @description
 * # CourseListCtrl
 * Controller of the sespaApp
 */
angular.module('sespaApp')
  .controller('CourseListCtrl', function(advisingData, $scope, $routeParams) {
    $scope.courseListHeader = null;
    $scope.student = null;
    $scope.sortType = 'class_site.description';
    $scope.sortReverse = false;
    $scope.searchStudent = '';
    // $scope.scroll = scroll;

    $scope.courses = [];

    advisingData.studentCourses($routeParams.student).then(function(course) {
      $scope.courses = course;
    });
    
    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.courseListHeader = student.first_name + ' ' + student.last_name;
      $scope.student = student;
    });
    
  });
