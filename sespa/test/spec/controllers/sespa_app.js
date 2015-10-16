'use strict';

describe('Controller: SespaAppCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var SespaAppCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SespaAppCtrl = $controller('SespaAppCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(SespaAppCtrl.awesomeThings.length).toBe(3);
  });
});
