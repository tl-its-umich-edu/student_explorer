'use strict';

describe('Controller: CourseDetailCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var CourseDetailCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    CourseDetailCtrl = $controller('CourseDetailCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(CourseDetailCtrl.awesomeThings.length).toBe(3);
  });
});
