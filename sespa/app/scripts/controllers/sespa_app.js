'use strict';

/**
 * @ngdoc function
 * @name sespaApp.controller:SespaAppCtrl
 * @description
 * # SespaAppCtrl
 * Controller of the sespaApp
 */
 
function appendAlert(reason) {
  var alertDiv = angular.element( document.querySelector( '.alert-container' ) );
  alertDiv.append('<div class="alert alert-danger alert-dismissible" role="alert">' +
    '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
    '<strong>Warning!</strong> ' + reason + '</div>');
}

angular.module('sespaApp')
  .controller('SespaAppCtrl', function(advisingData, $scope, $location) {
    advisingData.config().then(function(config) {
      $scope.config = config;
      $scope.studentSearch = function() {
        $location.path('/students').search({search: $scope.search});
      };
    });
    
    advisingData.userInfo().then(function(userInfo) {
      $scope.userInfo = userInfo;
    }, function(reason) {
      // window.alert(reason);
      appendAlert(reason);
    });
  });
