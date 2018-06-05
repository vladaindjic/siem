import { Component, OnInit } from '@angular/core';
import { AlarmsService } from '../../services/alarms/alarms.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { IAlarm } from '../../model/IAlarm';

@Component({
  selector: 'app-alarms',
  templateUrl: './alarms.component.html',
  styleUrls: ['./alarms.component.css']
})
export class AlarmsComponent implements OnInit {

  alarmi: IAlarm[]
  showAlarm
  createAlarmForm: FormGroup;
  updateAlarmForm: FormGroup;
  temporaryId
  temporaryIndex

  constructor(private alarmsService: AlarmsService,
    private route: ActivatedRoute,
    private router: Router,
    private toastr: ToastrService,
    private fb: FormBuilder) { }

  ngOnInit() {
    this.route.queryParams.subscribe((params) => {
      let query = params['query'];
      this.alarmsService.getAlarms().subscribe((data) => {
        this.alarmi = JSON.parse(data.toString());
        this.showAlarm = true
      });
    })
    this.createForm();
    this.createUpdateForm('');
  }

  createForm() {
    this.createAlarmForm = this.fb.group({
      query: ['', Validators.required]
    }, { updateOn: 'submit' });
  }

  createUpdateForm(queryText) {
    this.updateAlarmForm = this.fb.group({
      query: [queryText, Validators.required]
    }, { updateOn: 'submit' });
  }

  addNewAlarm() {
    const newAlarm = this.createAlarmForm.value;
    this.alarmsService.createAlarm(newAlarm)
      .subscribe(data => {
        this.toastr.success('Your Alarm is successfully created!');
        this.ngOnInit();
      },
        (err: HttpErrorResponse) => {
          if (err.error instanceof Error) {
            this.toastr.error(err.error.message + '\nError Status ' + err.status);
          } else {
            this.toastr.error(err.error.message + '\nError Status ' + err.status);
          }
        });
  }

  deleteAlarm(idA, index) {
    this.alarmsService.deleteAlarm(idA)
      .subscribe(data => {
        this.toastr.success('Your alarm is successfully deleted!');
        this.createForm();
        this.alarmi.splice(index, 1);
        this.showAlarm = true

      },
        (err: HttpErrorResponse) => {
          if (err.error instanceof Error) {
            this.toastr.error(err.error.message + '\nError Status ' + err.status);
          } else {
            this.toastr.error(err.error.message + '\nError Status ' + err.status);
          }
        });
  }

  updateAlarm() {
    if (this.temporaryId === null || this.temporaryIndex === null) {
      this.cancelUpdate()
    }
    const updatedAlarm = this.updateAlarmForm.value;
    this.alarmsService.updateAlarm(this.temporaryId,updatedAlarm)
      .subscribe(data => {
        this.alarmi[this.temporaryIndex].query = JSON.parse(data.toString()).query
        this.toastr.success('Your alarm is successfully updated!');
        this.createForm();
        this.showAlarm = true

      },
        (err: HttpErrorResponse) => {
          if (err.error instanceof Error) {
            this.toastr.error(err.error.message + '\nError Status ' + err.status);
          } else {
            this.toastr.error(err.error.message + '\nError Status ' + err.status);
          }
        });

  }

  showUpdate(alarm, index) {
    this.createUpdateForm(alarm.query)
    this.temporaryId = alarm._id.$oid
    this.temporaryIndex = index;
    this.showAlarm = false;
  }
  cancelUpdate() {
    this.showAlarm = true;
    this.temporaryId = null
    this.temporaryIndex = null
  }

}
