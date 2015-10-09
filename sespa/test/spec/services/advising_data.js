'use strict';

describe('Service: advisingData', function () {

  // load the service's module
  beforeEach(module('sespaApp'));

  // instantiate service
  var advisingData;
  beforeEach(inject(function (_advisingData_) {
    advisingData = _advisingData_;
  }));

  it('should do something', function () {
    expect(!!advisingData).toBe(true);
  });

});
