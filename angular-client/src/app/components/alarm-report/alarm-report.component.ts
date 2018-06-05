import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import * as moment from 'moment';
import { LogService } from '../../services/log.service';

@Component({
  selector: 'app-alarm-report',
  templateUrl: './alarm-report.component.html',
  styleUrls: ['./alarm-report.component.css']
})
export class AlarmReportComponent implements OnInit {
  
  public selectedMoments = [];
  public selectedHost;
  public hosts =['All'];
  public report;
  constructor(private logService:LogService) {
   }
 
  ngOnInit() {
    this.logService.getHosts().subscribe((data)=>{
      console.log(data);
      this.hosts = this.hosts.concat(data as Array<any>);
    })
  }


  getReport(){
    let data = {};
    data['startTime'] = moment(this.selectedMoments[0]).format();
    data['endTime'] = moment(this.selectedMoments[1]).format();
    if(this.selectedHost.includes('All')){
      data['all'] = true;
    }else{
      data['all'] = false;
    }
    data['hosts'] = this.selectedHost;
    //console.log(data);
    this.logService.getAlarmAnalytics(data).subscribe((data)=>{
      data = JSON.parse(data as string);
      console.log(data);
      this.report = data;
    })
  }

}
