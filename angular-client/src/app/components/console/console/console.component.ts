import { Component, OnInit } from '@angular/core';
import {ILog} from '../../../model/ILog';
import {SharedLogService} from '../../../services/shared-log/shared-log.service';

@Component({
  selector: 'app-console',
  templateUrl: './console.component.html',
  styleUrls: ['./console.component.css']
})
export class ConsoleComponent implements OnInit {

  receivedLogs: ILog[] = [];
  constructor(private sharedLogService: SharedLogService) {}

  ngOnInit() {
    this.receivedLogs = this.sharedLogService.logs;
  }

  clearConsole(){
    this.sharedLogService.clearLogs();
    this.receivedLogs = this.sharedLogService.logs;
  }

}
