import { Injectable } from '@angular/core';
import {ILocation} from 'selenium-webdriver';
import {ILog} from '../../model/ILog';

@Injectable()
export class SharedLogService {

  public logs: ILog[] = [];
  public alarmFires: Object[] = [];

  constructor() { }

  addLog(log: ILog){
    this.logs.unshift(log);
  }

  clearLogs(){
    this.logs = [];
  }

  addAlarmFire(alarmFire: Object){
    this.alarmFires.unshift(alarmFire);

  }

  clearAlarmFires(){
    this.alarmFires = [];
  }

}
