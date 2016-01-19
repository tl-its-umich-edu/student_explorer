'use strict';

/**
 * @ngdoc directive
 * @name sespaApp.directive:bootstrapStatusTooltip
 * @description
 * # bootstrapStatusTooltip
 */
angular.module('sespaApp')
  .directive('statusTooltip', function(){
    return {
      restrict: 'A',
      link: function(scope, element, attrs){
        $(element).hover(function(){
          // on mouseenter
          if (element.context.title === 'Green') {
            element.context.title = 'Encourage';
          } else if (element.context.title === 'Yellow') {
            element.context.title = 'Explore';
          } else if (element.context.title === 'Red') {
            element.context.title = 'Engage';
          }
          $(element).tooltip('show');
        }, function(){
          // on mouseleave
          $(element).tooltip('hide');
        });
      }
    };
  });
