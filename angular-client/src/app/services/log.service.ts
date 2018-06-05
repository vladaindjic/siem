import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable()
export class LogService {

  constructor(private http: HttpClient) { }

  logSearch(text: string) {
    let params = new HttpParams();
    params = params.append('query', text);
    const url = `/api/center/find_logs`;
    return this.http.get(url,{params:params});
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

}
