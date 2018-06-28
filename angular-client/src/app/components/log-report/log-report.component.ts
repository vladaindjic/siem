import { Component, OnInit, Input, Output, EventEmitter, ViewChild, ElementRef } from '@angular/core';
import * as moment from 'moment';
import { LogService } from '../../services/log.service';
import { ToastrService } from 'ngx-toastr';
// import * as jsPDF from 'jspdf-autotable';
// import * as html2canvas from 'html2canvas';
declare let jsPDF;
// declare var html2pdf: any;


@Component({
  selector: 'app-log-report',
  templateUrl: './log-report.component.html',
  styleUrls: ['./log-report.component.css']
})
export class LogReportComponent implements OnInit {
  @ViewChild('report') el: ElementRef;
  public selectedMoments = [];
  public selectedHost;
  public hosts = ['All'];
  public report;
  public logs = [];

  public config = {
    search: true //enables the search plugin to search in the list
  };

  constructor(private logService: LogService, private toastr: ToastrService) { }

  ngOnInit() {
    this.logService.getHosts().subscribe((data) => {
      this.hosts = this.hosts.concat(data as Array<any>);
    })
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
    this.logService.getLogAnalytics(data).subscribe((data) => {
      data = JSON.parse(data as string);
      if (data['count'] === 0) {
        this.toastr.error('0 results for this query')
      } else {
        this.report = data;
        this.logs = [];
        for (let aggregation of data['aggregations']) {
          this.logs = this.logs.concat(aggregation.logs);
        }
      }
    },
      (error) => {
        this.toastr.error('Incorrect use of query');
      })
  }

  selectionChanged(eventValue) {
  }

  savePDF() {

    // let pdf = new jsPDF();

    // pdf.addHTML(this.el.nativeElement, () => {
    //   pdf.save("test1.pdf");
    // });

    // let doc = new jsPDF();

    // // Add a title to your PDF
    // doc.setFontSize(30);
    // doc.text(12, 10, "Your Title");

    // Create your table here (The dynamic table needs to be converted to canvas).
    // let element = <HTMLScriptElement>document.getElementsByClassName("pvtTable")[0];
    // html2canvas(element)
    //   .then((canvas: any) => {
    //     doc.addImage(canvas.toDataURL("image/jpeg"), "JPEG", 0, 50, doc.internal.pageSize.width, element.offsetHeight / 5);
    //     doc.save(`Report-${Date.now()}.pdf`);
    //   })

    //   html2canvas(("#canvas"), {
    //     onrendered: function(canvas) {
    //         var imgData = canvas.toDataURL(
    //             'image/png');
    //         var doc = new jsPDF('p', 'mm');
    //         doc.addImage(imgData, 'PNG', 10, 10);
    //         doc.save('sample-file.pdf');
    //     }
    // });
    var doc = new jsPDF('p', 'pt','a4');
    var cols = ["appname", "facility", "hostname", "severity", "timestamp", "msg"];
    var rows = [];

    for (var log of this.logs) {
      var temp = [log['appname'], log['facility'], log['hostname'], log['severity'], moment(log['timestamp']).format(), log['msg']];
      rows.push(temp);
    }

    // doc.autoTable(cols, rows, {
    //     margin: {horizontal: 7},
    //     bodyStyles: {valign: 'top'},
    //     styles: {overflow: 'linebreak', columnWidth: 'wrap'},
    //     columnStyles: {text: {columnWidth: 'auto'}}
    // });

    doc.autoTable(cols, rows, {styles: {overflow: 'linebreak'},columnStyles: {
      0: {columnWidth: 80},
      1: {columnWidth: 50},
      2: {columnWidth: 80},
      3: {columnWidth: 50},
      4: {columnWidth: 90},
      5: {columnWidth: 180},
  }});
    let name = "repot_" + moment(new Date).format();
    doc.save(name + '.pdf');
    // return doc;
  }
}
