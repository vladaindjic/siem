import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class LogService {

  constructor(private http: HttpClient) { }

  logSearch(text:string){
    // const url=`/api/logger?query=${text}`;
    const url=`/api/logger/all`;
    return this.http.get(url);
  }

}
