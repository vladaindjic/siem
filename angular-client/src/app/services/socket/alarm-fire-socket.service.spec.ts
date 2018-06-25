import { TestBed, inject } from '@angular/core/testing';

import { AlarmFireSocketService } from './alarm-fire-socket.service';

describe('AlarmFireSocketService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AlarmFireSocketService]
    });
  });

  it('should be created', inject([AlarmFireSocketService], (service: AlarmFireSocketService) => {
    expect(service).toBeTruthy();
  }));
});
