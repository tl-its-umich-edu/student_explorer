'use strict';

describe('Controller: StudentcontrollerCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var StudentcontrollerCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    StudentcontrollerCtrl = $controller('StudentcontrollerCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(StudentcontrollerCtrl.awesomeThings.length).toBe(3);
  });
});
