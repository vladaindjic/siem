import { Injectable } from '@angular/core';
import {ILocation} from 'selenium-webdriver';
import {ILog} from '../../model/ILog';

@Injectable()
export class SharedLogService {

  public logs: ILog[] = [];

  constructor() { }

  addLog(log: ILog){
    this.logs.unshift(log);
  }

  clearLogs(){
    this.logs = [];
  }

}
