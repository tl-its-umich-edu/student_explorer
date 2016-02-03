'use strict';

/**
 * @ngdoc service
 * @name sespaApp.advisingUtilities
 * @description
 * # advisingUtilities
 * Factory in the sespaApp.
 */
angular.module('sespaApp')
  .factory('advisingUtilities', function() {
    // Service logic

    // Public API here
    return {
      updateProgress: function(update, scope) {
        if (typeof update === 'number') {
          scope.progress = update * 100;
        }
      },
      alert: function(reason, type) {
        if (typeof type === 'undefined') {
          type = 'warning';
        }
        var alertDiv = angular.element(document.querySelector('.alert-container'));
        alertDiv.append('<div class="alert alert-' + type + ' alert-dismissible" role="alert">' +
          '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
          reason + '</div>');
      },
      httpErrorHandler: function(reason, scope, setNotFound) {
        console.log(reason);
        var displayAlert = false;
        if (typeof scope === 'object') {
          if (reason.status === 404) {
            if (setNotFound) {
              scope.notFound = true;
            }
            displayAlert = false;
          }
          if (reason.status >= 500) {
            scope.$parent.dataDown = true;
          }
        }

        if (displayAlert) {
          this.alert('<strong>' + reason.statusText + '</strong> ' + reason.config.url + ' (' + reason.status + ')');
        }

      },
    };
  });
