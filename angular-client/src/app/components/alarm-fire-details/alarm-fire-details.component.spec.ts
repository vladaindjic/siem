import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlarmFireDetailsComponent } from './alarm-fire-details.component';

describe('AlarmFireDetailsComponent', () => {
  let component: AlarmFireDetailsComponent;
  let fixture: ComponentFixture<AlarmFireDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlarmFireDetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlarmFireDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
