'use strict';

describe('Controller: AdvisorDetailCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var AdvisorDetailCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    AdvisorDetailCtrl = $controller('AdvisorDetailCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(AdvisorDetailCtrl.awesomeThings.length).toBe(3);
  });
});
