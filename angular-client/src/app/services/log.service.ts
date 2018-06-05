import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import {Observer} from "rxjs/Observer";
import {Observable} from "rxjs/Observable";
import {ILog} from "../model/ILog";
import {IFindLogsResult} from "../model/IFindLogsResult";
import {IQueryDto} from "../model/IQueryDto";

@Injectable()
export class LogService {

  queryDto: IQueryDto;

  constructor(private http: HttpClient) {
    this.queryDto = {query: ""};
  }

  logSearch(text: string = this.queryDto.query): Observable<IFindLogsResult> {
    console.log('Ovo trazimo: ', text);
    const url = `/api/center/find_logs`;
    // return this.http.get<IFindLogsResult>(url,{params:params});
    return this.http.put<IFindLogsResult>(url, {"query": text});

  }

  getHosts(){
    const url = '/api/center/get_hosts';
    return this.http.get(url);
  }


  getAlarmAnalytics(data){
    const url = 'api/center/get_alarm_analytics';
    return this.http.put(url,data);
  }

  getLogAnalytics(data){
    const url = 'api/center/get_log_analytics';
    return this.http.put(url,data);
  }

  setQuery(query: string){
    this.queryDto.query = query;
  }

}
