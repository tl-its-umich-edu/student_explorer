'use strict';

/**
 * @ngdoc directive
 * @name sespaApp.directive:windowResize
 * @description
 * # windowResize
 */
angular.module('sespaApp')
  .directive('windowResize', function ($window) {
    return {
      restrict: 'A',
      link: function(scope, element, attrs) {
        scope.$watch(function() {
            scope.windowWidth = window.innerWidth;
        });
        
        angular.element($window).bind('resize', function() {
          scope.$apply();
        });
      }
    };
  });
