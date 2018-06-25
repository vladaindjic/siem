import { Injectable } from '@angular/core';
import {AlarmFireSocketClass} from './AlarmFireSocketClass';
import {ToastrService} from 'ngx-toastr';

@Injectable()
export class AlarmFireSocketService {

  static socektLocation = 'wss://localhost/alarm-fire';
  // static socektLocation = 'ws://localhost/alarm-fire';

  sockets = {};

  constructor(private toastr: ToastrService) { }

  openSocket(username: string) {
    console.log('Otvaramo socket za korisnika: ' + username);
    if (this.sockets[username]) {
      this.closeSocket(username);
    }
    this.sockets[username] = new AlarmFireSocketClass(AlarmFireSocketService.socektLocation, this.toastr);
  }

  closeSocket(username: string) {
    console.log('Treba ugasiti socket za sledeceg korisnika ' + username);
    if (this.sockets[username]) {
      (this.sockets[username] as AlarmFireSocketClass).closeSocket();
      this.sockets[username] = null;
    }
  }
}