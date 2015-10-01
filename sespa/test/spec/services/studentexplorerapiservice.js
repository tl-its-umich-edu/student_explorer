'use strict';

describe('Service: StudentExplorerApiService', function () {

  // load the service's module
  beforeEach(module('sespaApp'));

  // instantiate service
  var StudentExplorerApiService;
  beforeEach(inject(function (_StudentExplorerApiService_) {
    StudentExplorerApiService = _StudentExplorerApiService_;
  }));

  it('should do something', function () {
    expect(!!StudentExplorerApiService).toBe(true);
  });

});
