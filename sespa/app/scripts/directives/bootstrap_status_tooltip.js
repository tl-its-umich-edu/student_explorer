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
      restrict: 'E',
      scope: {
        statusOutput: '=status'
      },
      link: function(scope, element, attrs){
        $(element).hover(function(){
          // on mouseenter
          if (element.context.childNodes[0].classList[1] === 'green') {
            element.context.title = 'Encourage';
          } else if (element.context.childNodes[0].classList[1] === 'yellow') {
            element.context.title = 'Explore';
          } else if (element.context.childNodes[0].classList[1] === 'red') {
            element.context.title = 'Engage';
          }
          element.context.alt = element.context.title;
          element.context.dataset.placement = 'bottom';
          $(element).tooltip('show');
        }, function(){
          // on mouseleave
          $(element).tooltip('hide');
        });
      },
      templateUrl: 'views/status_image.html'
    };
  });
