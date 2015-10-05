'use strict';

describe('Service: StudentService', function () {

  // load the service's module
  beforeEach(module('sespaApp'));

  // instantiate service
  var StudentService;
  beforeEach(inject(function (_StudentService_) {
    StudentService = _StudentService_;
  }));

  it('should do something', function () {
    expect(!!StudentService).toBe(true);
  });

});
