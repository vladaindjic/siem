import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Injectable, Injector } from '@angular/core';
import { LoggedUtils } from '../utils/logged-utils';

@Injectable()
export class TokenInterceptorService {

  constructor(private inj: Injector) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    request = request.clone({
      setHeaders: {
        'Content-Type': 'application/xml',
        'X-Auth-Token': LoggedUtils.getToken(),
      },
    });
    console.log(request);
    return next.handle(request);
  }

}
