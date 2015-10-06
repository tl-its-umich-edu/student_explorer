'use strict';

describe('Service: studentExplorer', function () {

  // load the service's module
  beforeEach(module('sespaApp'));

  // instantiate service
  var studentExplorer;
  beforeEach(inject(function (_studentExplorer_) {
    studentExplorer = _studentExplorer_;
  }));

  it('should do something', function () {
    expect(!!studentExplorer).toBe(true);
  });

});
