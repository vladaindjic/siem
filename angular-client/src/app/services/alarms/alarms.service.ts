import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { IAlarm } from '../../model/IAlarm'; 
import { Observable } from 'rxjs/Observable';

@Injectable()
export class AlarmsService {

  constructor(private http: HttpClient) { }

  createAlarm(query) {
    return this.http.post('/api/center/create_alarm', query);
  }

  updateAlarm(idA, query) {
    return this.http.put<IAlarm>(`/api/center/update_alarm/${idA}`, query);
  }

  deleteAlarm(idA) {
    return this.http.delete(`/api/center/delete_alarm/${idA}`);
  }

  getAlarms(): Observable<IAlarm[]> {
    return this.http.get<IAlarm[]>('/api/center/get_alarms');
  }

  getAlarm(idA) {
    return this.http.get(`/api/center/get_alarm_details?id=${idA}`);
  }
}
