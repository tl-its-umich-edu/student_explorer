'use strict';

describe('Controller: ClassSiteListCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var ClassSiteListCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ClassSiteListCtrl = $controller('ClassSiteListCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(ClassSiteListCtrl.awesomeThings.length).toBe(3);
  });
});
