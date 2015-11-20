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
    $scope.assignments = null;
    $scope.courseHistory = null;
    $scope.historyLength = null;
    $scope.historyDate = null;
    $scope.courseDescription = null;
    $scope.sortTypeAssignment = 'assignment.description';
    $scope.sortTypeHistory = 'date';
    $scope.sortReverse = false;
    $scope.searchStudent = '';
    // $scope.scroll = scroll;

    advisingData.studentCourses($routeParams.student).then(function(courses){
      courses.forEach(function(course){
        if (course.class_site.code === $routeParams.courseCode) {
          $scope.courseDescription = course.class_site.description;
        }
      });
    });

    advisingData.studentCourseAssignments($routeParams.student, $routeParams.courseCode).then(function(assignment) {
      $scope.assignments = assignment;
    });
    
    advisingData.studentCourseHistory($routeParams.student, $routeParams.courseCode).then(function(courseHistory) {
      $scope.courseHistory = courseHistory;
      $scope.historyDate = Object.keys(courseHistory);
      $scope.historyLength = $scope.historyDate.length;
    });
    
    advisingData.studentDetails($routeParams.student).then(function(student) {
      $scope.courseDetailHeader = student.first_name + ' ' + student.last_name;
    });
    
  });
