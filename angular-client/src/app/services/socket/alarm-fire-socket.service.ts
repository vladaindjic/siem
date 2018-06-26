import { Injectable } from '@angular/core';
import {AlarmFireSocketClass} from './AlarmFireSocketClass';
import {ToastrService} from 'ngx-toastr';
import {Router} from '@angular/router';
import {SharedLogService} from '../shared-log/shared-log.service';

@Injectable()
export class AlarmFireSocketService {

  static socektLocation = 'wss://192.168.0.17/alarm-fire/';
  // static socektLocation = 'ws://localhost/alarm-fire';
  static logSocketLocation = 'wss://192.168.0.17/log/';

  sockets = {};

  constructor(private toastr: ToastrService,
              private router: Router,
              private sharedLogService: SharedLogService) { }

  openSocket(username: string) {
    console.log('Otvaramo socket za korisnika: ' + username);
    if (this.sockets[username]) {
      this.closeSocket(username);
    }
    this.sockets[username] = new AlarmFireSocketClass(AlarmFireSocketService.socektLocation, this.toastr, this.router,
      AlarmFireSocketService.logSocketLocation, this.sharedLogService);
  }

  closeSocket(username: string) {
    console.log('Treba ugasiti socket za sledeceg korisnika ' + username);
    if (this.sockets[username]) {
      (this.sockets[username] as AlarmFireSocketClass).closeSocket();
      this.sockets[username] = null;
    }
  }
}
