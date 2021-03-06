import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { HttpParams } from '@angular/common/http/src/params';
import 'rxjs/add/observable/throw';
import 'rxjs/add/operator/map';

@Injectable()
export class AuthenticationService {

  constructor(private http: HttpClient) { }

  authenticateUser(userLogin) {
    return this.http.post('/api/center/login', userLogin);
  }

  changeUserPass(passWord){
    return this.http.put('/api/center/change_password', passWord);
  }

}
