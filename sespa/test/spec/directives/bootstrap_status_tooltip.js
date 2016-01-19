'use strict';

describe('Directive: bootstrapStatusTooltip', function () {

  // load the directive's module
  beforeEach(module('sespaApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<bootstrap-status-tooltip></bootstrap-status-tooltip>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the bootstrapStatusTooltip directive');
  }));
});
