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

}
