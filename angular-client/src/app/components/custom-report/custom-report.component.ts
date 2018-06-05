import { Component, OnInit, Output, Input, EventEmitter } from '@angular/core';
import { LogService } from '../../services/log.service';
import * as moment from 'moment';
import { ToastrService } from 'ngx-toastr';

declare let jsPDF;

@Component({
  selector: 'app-custom-report',
  templateUrl: './custom-report.component.html',
  styleUrls: ['./custom-report.component.css']
})
export class CustomReportComponent implements OnInit {

  constructor(private logService: LogService, private toastr: ToastrService) { }

  public query: string;
  public report;
  public logs;
  ngOnInit() {
  }

  getReport() {
    // console.log(this.query);
    this.logService.logSearch(this.query).subscribe((data) => {
      data = JSON.parse(data as string);
      console.log(data);
      if (data['count'] === 0) {
        this.toastr.error('0 results for this query')
      } else {
        this.report = data;
        for (let aggregation of data['aggregations']) {
          this.logs = this.logs.concat(aggregation.logs);
        }
      }
    },
      (error) => {
        this.toastr.error('Incorrect use of query');
      });
  }

  savePDF() {
    var doc = new jsPDF('1', 'pt', 'a4');
    var col = ["appname", "facility", "hostname", "severity", "timestamp", "msg"];
    var rows = [];

    for (var log of this.logs) {
      var temp = [log['appname'], log['facility'], log['hostname'], log['severity'], moment(log['timestamp']).format(), log['msg']];
      rows.push(temp);
    }
    console.log(col)
    console.log(rows)
    doc.autoTable(col, rows, {
      tableWidth: 'auto',
      headerStyles: { columnWidth: 'auto' },
      bodyStyles: { overflow: 'linebreak', columnWidth: 'wrap' },
      columnStyles: { text: { columnWidth: 'wrap' } },
    });
    let name = "repot_" + moment(new Date).format();
    doc.save(name + '.pdf');
    return doc;
  }
}
