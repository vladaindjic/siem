import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class LogService {

  constructor(private http: HttpClient) { }

  logSearch(text:string){
    const url=`/api/center/find_logs?query=${text}`;
    return this.http.get(url);
  }

}
