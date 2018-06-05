import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {


  public show;
  constructor() { 
    this.show = 'logReports';
  }

  ngOnInit() {
  }

  togleReports(reportsToShow){
    this.show = reportsToShow;
  }
 

}
