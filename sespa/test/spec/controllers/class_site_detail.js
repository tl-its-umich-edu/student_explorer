'use strict';

describe('Controller: ClassSiteDetailCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var ClassSiteDetailCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ClassSiteDetailCtrl = $controller('ClassSiteDetailCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(ClassSiteDetailCtrl.awesomeThings.length).toBe(3);
  });
});
