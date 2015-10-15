'use strict';

describe('Controller: StudentDetailCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var StudentDetailCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    StudentDetailCtrl = $controller('StudentDetailCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(StudentDetailCtrl.awesomeThings.length).toBe(3);
  });
});
