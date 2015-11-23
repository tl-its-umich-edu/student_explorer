'use strict';

describe('Service: advisingUtilities', function () {

  // load the service's module
  beforeEach(module('sespaApp'));

  // instantiate service
  var advisingUtilities;
  beforeEach(inject(function (_advisingUtilities_) {
    advisingUtilities = _advisingUtilities_;
  }));

  it('should do something', function () {
    expect(!!advisingUtilities).toBe(true);
  });

});
