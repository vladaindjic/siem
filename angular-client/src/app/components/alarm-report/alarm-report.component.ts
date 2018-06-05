import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';
import { FormGroup, FormBuilder } from '@angular/forms';
@Component({
  selector: 'app-alarm-report',
  templateUrl: './alarm-report.component.html',
  styleUrls: ['./alarm-report.component.css']
})
export class AlarmReportComponent implements OnInit {
  
 
  public selectedMoments = [];
  public selectedHost;
  public hosts =['All','host1','host2','host3','host4'];
  form:FormGroup;

  constructor(private fb:FormBuilder) {
   }
 
  ngOnInit() {
    
    this.form = this.fb.group({
      hosts: this.fb.array([])
    })
  }


  getReport(){
    console.log(this.selectedHost);
    console.log(moment(this.selectedMoments[1]).format());
  }

  

}
