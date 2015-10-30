'use strict';

describe('Controller: StudentSearchCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var StudentSearchCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    StudentSearchCtrl = $controller('StudentSearchCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(StudentSearchCtrl.awesomeThings.length).toBe(3);
  });
});
