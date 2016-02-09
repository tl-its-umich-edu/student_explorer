'use strict';

describe('Controller: StudentClassSiteListCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var StudentClassSiteListCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    StudentClassSiteListCtrl = $controller('StudentClassSiteListCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(StudentClassSiteListCtrl.awesomeThings.length).toBe(3);
  });
});
