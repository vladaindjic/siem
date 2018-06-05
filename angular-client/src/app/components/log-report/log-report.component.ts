import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import * as moment from 'moment';
import { LogService } from '../../services/log.service';
import { ToastrService } from 'ngx-toastr';

declare let jsPDF;


@Component({
  selector: 'app-log-report',
  templateUrl: './log-report.component.html',
  styleUrls: ['./log-report.component.css']
})
export class LogReportComponent implements OnInit {

  public selectedMoments = [];
  public selectedHost;
  public hosts =['All'];
  public report;
  constructor(private logService:LogService,private toastr:ToastrService) { }

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
    this.logService.getLogAnalytics(data).subscribe((data)=>{
      data = JSON.parse(data as string);
      console.log(data);
      if(data['count']===0){
        this.toastr.error('0 results for this query')
      }else{
        this.report = data['aggregations'][0];
      }
    },
    (error) => {
      this.toastr.error('Incorrect use of query');
    })
  }

  savePDF(){
    var doc = new jsPDF('1', 'pt','a4');
    var col = ["appname", "facility","hostname","severity","timestamp","msg"];
    var rows = [];

    for(var log of this.report['logs']){
        var temp = [log['appname'],log['facility'],log['hostname'],log['severity'],moment(log['timestamp']).format(),log['msg']];
        rows.push(temp);
    }
    console.log(col)
    console.log(rows)
    doc.autoTable(col, rows,{
      tableWidth: 'auto',
      headerStyles:{columnWidth:'auto'},
      bodyStyles: {overflow: 'linebreak', columnWidth: 'wrap'},
      columnStyles: {text: {columnWidth: 'wrap'}},
  });
  let name = "repot_"+  moment(new Date).format();
  doc.save(name+'.pdf');
  return doc;
}
}
