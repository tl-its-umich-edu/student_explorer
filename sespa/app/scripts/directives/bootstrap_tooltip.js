'use strict';

/**
 * @ngdoc directive
 * @name sespaApp.directive:bootstrapTooltip
 * @description
 * # bootstrapTooltip
 */
angular.module('sespaApp')
  .directive('tooltip', function(){
    return {
      restrict: 'A',
      link: function(scope, element, attrs){
        $(element).hover(function(){
          // on mouseenter
          $(element).tooltip('show');
        }, function(){
          // on mouseleave
          $(element).tooltip('hide');
        });
      }
    };
  });
