import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlarmReportComponent } from './alarm-report.component';

describe('AlarmReportComponent', () => {
  let component: AlarmReportComponent;
  let fixture: ComponentFixture<AlarmReportComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlarmReportComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlarmReportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
