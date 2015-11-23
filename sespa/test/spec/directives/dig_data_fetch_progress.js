'use strict';

describe('Directive: digDataFetchProgress', function () {

  // load the directive's module
  beforeEach(module('sespaApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<dig-data-fetch-progress></dig-data-fetch-progress>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the digDataFetchProgress directive');
  }));
});
