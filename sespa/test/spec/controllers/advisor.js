'use strict';

describe('Controller: AdvisorcontrollerCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var AdvisorcontrollerCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    AdvisorcontrollerCtrl = $controller('AdvisorcontrollerCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(AdvisorcontrollerCtrl.awesomeThings.length).toBe(3);
  });
});
