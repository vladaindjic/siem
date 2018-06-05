import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {


  public show;
  public noReportToShow;
  public report;
  constructor() { 
    this.show = 'logReports';
    this.noReportToShow = true;
  }

  ngOnInit() {
    this.noReportToShow = true;
  }

  onShowReport(data){
    console.log(data);
    this.report = data;
    this.noReportToShow =false;
  }

  togleReports(reportsToShow){
    this.show = reportsToShow;
  }
 

}
