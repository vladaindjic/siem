import {ToastrService} from 'ngx-toastr';
import {Router} from '@angular/router';
import {SharedLogService} from '../shared-log/shared-log.service';

export class AlarmFireSocketClass {
  socketUrl: string;
  socket: WebSocket;
  toastr: ToastrService;
  router: Router;

  logSocketUrl: string;
  logSocket: WebSocket;

  sharedLogService: SharedLogService;

  constructor(socketUrl: string, toastr: ToastrService, router: Router, logSocketUrl: string, sharedLogService: SharedLogService) {
    this.sharedLogService = sharedLogService;
    this.sharedLogService.clearLogs();
    this.sharedLogService.clearAlarmFires();

    this.socketUrl = socketUrl;
    this.openSocket();
    this.toastr = toastr;
    this.router = router;

    this.logSocketUrl = logSocketUrl;
    this.openLogSocket();
  }

  openSocket() {
    this.socket = new WebSocket(this.socketUrl);

    this.socket.onmessage = ev => {
      // poruke da je otvoren ili zatvoren socket
      if (ev.data === 'connected' || ev.data === 'disconnected') {
        return;
      }
      // prikazivanje toastr-a
       this.sharedLogService.addAlarmFire(JSON.parse(ev.data));

    };

    this.socket.onopen = () => {

    };
    this.socket.onclose = () => {

    };
  }

  openLogSocket(){
    this.logSocket = new WebSocket(this.logSocketUrl);

    this.logSocket.onmessage = ev => {
      // poruke da je otvoren ili zatvoren socket
      if (ev.data === 'connected' || ev.data === 'disconnected') {
        return;
      }
      // dodajemo log
      this.sharedLogService.addLog(JSON.parse(ev.data));
    };

    this.logSocket.onopen = () => {
    };
    this.logSocket.onclose = () => {
    };
  }


  closeSocket() {
    this.socket.close();
    this.logSocket.close();
  }

}
