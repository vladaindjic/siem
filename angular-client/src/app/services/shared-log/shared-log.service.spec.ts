import { TestBed, inject } from '@angular/core/testing';

import { SharedLogService } from './shared-log.service';

describe('SharedLogService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SharedLogService]
    });
  });

  it('should be created', inject([SharedLogService], (service: SharedLogService) => {
    expect(service).toBeTruthy();
  }));
});
