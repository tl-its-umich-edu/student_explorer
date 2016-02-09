'use strict';

describe('Controller: StudentClassSiteDetailCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var StudentClassSiteDetailCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    StudentClassSiteDetailCtrl = $controller('StudentClassSiteDetailCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(StudentClassSiteDetailCtrl.awesomeThings.length).toBe(3);
  });
});
