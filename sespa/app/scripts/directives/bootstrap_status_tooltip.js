'use strict';

/**
 * @ngdoc directive
 * @name sespaApp.directive:bootstrapStatusTooltip
 * @description
 * # bootstrapStatusTooltip
 */
angular.module('sespaApp')
  .directive('statusTooltip', function () {
    return {
      restrict: 'E',
      scope: {
        status: '=status',
        tooltipText: '=tooltiptext'
      },
      link: function (scope, element) {
        $(element)
          .attr({
            'title': scope.tooltipText,
            'data-placement': 'bottom'
          })
          .hover(
            function () {
              // on mouseenter
              $(element).tooltip('show');
            }, function () {
              // on mouseleave
              $(element).tooltip('hide');
            }
          );
      },
      templateUrl: 'views/status_image.html'
    };
  });
