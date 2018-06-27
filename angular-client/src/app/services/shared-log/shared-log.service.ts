import { Injectable } from '@angular/core';
import {ILocation} from 'selenium-webdriver';
import {ILog} from '../../model/ILog';

@Injectable()
export class SharedLogService {

  public logs: ILog[] = [];

  constructor() { }

  addLog(log: ILog){
    console.log(log);
    this.logs.unshift(log);
    console.log(this.logs.length);
  }

  clearLogs(){
    this.logs = [];
  }

}
