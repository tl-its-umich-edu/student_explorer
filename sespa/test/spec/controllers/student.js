'use strict';

describe('Controller: StudentCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var StudentCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    StudentCtrl = $controller('StudentCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(StudentCtrl.awesomeThings.length).toBe(3);
  });
});
