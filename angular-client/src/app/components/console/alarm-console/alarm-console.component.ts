import { Component, OnInit } from '@angular/core';
import {SharedLogService} from '../../../services/shared-log/shared-log.service';
import {ILog} from '../../../model/ILog';
import {IAlarm} from '../../../model/IAlarm';
import {Router} from '@angular/router';

@Component({
  selector: 'app-alarm-console',
  templateUrl: './alarm-console.component.html',
  styleUrls: ['./alarm-console.component.css']
})
export class AlarmConsoleComponent implements OnInit {
  receivedAlarmLogs: Object[] = [];
  constructor(private sharedLogService: SharedLogService, private router: Router) { }

  ngOnInit() {
    this.receivedAlarmLogs = this.sharedLogService.alarmFires;
  }

  clearAlarmConsole(){
    this.sharedLogService.clearAlarmFires();
    this.receivedAlarmLogs = this.sharedLogService.alarmFires;
  }

  navigateTo(id:string){
    this.router.navigate(['alarm_fire_details/' + id]);
  }

}
