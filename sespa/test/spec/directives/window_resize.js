'use strict';

describe('Directive: windowResize', function () {

  // load the directive's module
  beforeEach(module('sespaApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<window-resize></window-resize>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the windowResize directive');
  }));
});
