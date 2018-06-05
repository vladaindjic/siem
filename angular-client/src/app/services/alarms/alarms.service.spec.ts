import { TestBed, inject } from '@angular/core/testing';

import { AlarmsService } from './alarms.service';

describe('AlarmsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AlarmsService]
    });
  });

  it('should be created', inject([AlarmsService], (service: AlarmsService) => {
    expect(service).toBeTruthy();
  }));
});
