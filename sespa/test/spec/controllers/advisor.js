'use strict';

describe('Controller: AdvisorCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var AdvisorCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    AdvisorCtrl = $controller('AdvisorCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(AdvisorCtrl.awesomeThings.length).toBe(3);
  });
});
