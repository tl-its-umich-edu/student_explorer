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
      alert: function(reason) {
        var alertDiv = angular.element(document.querySelector('.alert-container'));
        alertDiv.append('<div class="alert alert-danger alert-dismissible" role="alert">' +
          '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
          '<strong>Warning!</strong> ' + reason + '</div>');
      },
    };
  });
