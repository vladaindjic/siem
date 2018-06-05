import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';
@Component({
  selector: 'app-log-report',
  templateUrl: './log-report.component.html',
  styleUrls: ['./log-report.component.css']
})
export class LogReportComponent implements OnInit {

  public selectedMoments = [];
  public selectedHost;
  public hosts =['All','host1','host2','host3'];

  constructor() { }

  ngOnInit() {
  }

  getReport(){
    console.log(this.selectedHost);
    console.log(moment(this.selectedMoments[1]).format());
  }
}
