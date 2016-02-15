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
      restrict: 'A',
      scope: {
        status: '=status',
        tooltipText: '=tooltiptext'
      },
      link: function (scope, element) {
        $(element)
          .attr({
            'data-animation': false,
            'data-placement': 'bottom',
            'data-title': scope.tooltipText,
          })
          .tooltip();
      },
      templateUrl: 'views/status_image.html'
    };
  });
