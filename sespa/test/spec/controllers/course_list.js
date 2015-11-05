'use strict';

describe('Controller: CourseListCtrl', function () {

  // load the controller's module
  beforeEach(module('sespaApp'));

  var CourseListCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    CourseListCtrl = $controller('CourseListCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(CourseListCtrl.awesomeThings.length).toBe(3);
  });
});
