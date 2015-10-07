'use strict';

describe('Controller: StudentListCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var StudentListCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    StudentListCtrl = $controller('StudentListCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(StudentListCtrl.awesomeThings.length).toBe(3);
  });
});
