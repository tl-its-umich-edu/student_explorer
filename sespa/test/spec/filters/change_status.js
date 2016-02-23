'use strict';

describe('Filter: changeStatus', function () {

  // load the filter's module
  beforeEach(module('sespaApp'));

  // initialize a new instance of the filter before each test
  var changeStatus;
  beforeEach(inject(function ($filter) {
    changeStatus = $filter('changeStatus');
  }));

  it('should return the input prefixed with "changeStatus filter:"', function () {
    var text = 'angularjs';
    expect(changeStatus(text)).toBe('changeStatus filter: ' + text);
  });

});
