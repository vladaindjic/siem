import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import * as moment from 'moment';
import { LogService } from '../../services/log.service';

declare let jsPDF;

@Component({
  selector: 'app-alarm-report',
  templateUrl: './alarm-report.component.html',
  styleUrls: ['./alarm-report.component.css']
})
export class AlarmReportComponent implements OnInit {

  public selectedMoments = [];
  public selectedHost;
  public hosts = ['All'];
  public report;


  public config = {
    search: true //enables the search plugin to search in the list
  };


  constructor(private logService: LogService) {
  }

  ngOnInit() {
    this.logService.getHosts().subscribe((data) => {
      console.log(data);
      this.hosts = this.hosts.concat(data as Array<any>);
    })
  }

  selectionChanged(eventValue) {
    /*mozda nesto uradit*/
  }


  getReport() {
    let data = {};
    data['startTime'] = moment(this.selectedMoments[0]).format();
    data['endTime'] = moment(this.selectedMoments[1]).format();
    if (this.selectedHost.includes('All')) {
      data['all'] = true;
    } else {
      data['all'] = false;
    }
    data['hosts'] = this.selectedHost;
    //console.log(data);
    this.logService.getAlarmAnalytics(data).subscribe((data) => {
      data = JSON.parse(data as string);
      console.log(data);
      this.report = data;
    })
  }


  getPDF() {
    var cols = ["appname", "facility", "hostname", "severity", "timestamp", "msg"];
    var rows = [];
    let i = 1;
    var doc = new jsPDF('p', 'pt', 'a4');
    let pageHeight = 842;


    console.log(pageHeight);
    for (let aggregation of this.report.aggregations) {

      doc.setFontSize(12);
      doc.setTextColor(0);
      doc.setFontStyle('bold');

      doc.text(10, i * 20, 'On host ' + aggregation._id.hostname + ' alarm fires ' + aggregation.count);
      i++;
      if (i * 20 >= pageHeight) {
        doc.addPage();
        i = 1;
      }
      for (let alarm_fires of aggregation.alarm_fires) {
        doc.setFontSize(10);
        doc.setTextColor(0);
        doc.setFontStyle('normal');
        doc.text(20, i * 20, '- alarm string: ' + alarm_fires.alarm_str);
        i++;
        if (i * 20 >= pageHeight) {
          doc.addPage();
          i = 1;
        }
        rows = [];
        for (let log of alarm_fires.logs) {
          var temp = [log['appname'], log['facility'], log['hostname'], log['severity'], moment(log['timestamp']).format(), log['msg']];
          rows.push(temp);
        }
        doc.autoTable(cols, rows, {
          startY: i*20,
          styles: { overflow: 'linebreak' }, columnStyles: {
            0: { columnWidth: 80 },
            1: { columnWidth: 50 },
            2: { columnWidth: 80 },
            3: { columnWidth: 50 },
            4: { columnWidth: 90 },
            5: { columnWidth: 180 },
          }
        });
        i = doc.autoTable.previous.finalY/20;
        i++;

      }



    }
    doc.save('pera.pdf');
  }

}
