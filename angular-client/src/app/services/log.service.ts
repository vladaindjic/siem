import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import {Observer} from "rxjs/Observer";
import {Observable} from "rxjs/Observable";
import {ILog} from "../model/ILog";
import {IFindLogsResult} from "../model/IFindLogsResult";

@Injectable()
export class LogService {

  constructor(private http: HttpClient) { }

  logSearch(text: string): Observable<IFindLogsResult> {
    let params = new HttpParams();
    params = params.append('query', text);
    const url = `/api/center/find_logs`;
    return this.http.get<IFindLogsResult>(url,{params:params});
  }

}
