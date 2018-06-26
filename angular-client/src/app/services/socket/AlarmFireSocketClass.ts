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
    this.socketUrl = socketUrl;
    this.openSocket();
    this.toastr = toastr;
    this.router = router;

    this.logSocketUrl = logSocketUrl;
    this.openLogSocket();

    this.sharedLogService = sharedLogService;
  }

  openSocket() {
    this.socket = new WebSocket(this.socketUrl);

    this.socket.onmessage = ev => {
      // poruke da je otvoren ili zatvoren socket
      if (ev.data === 'connected' || ev.data === 'disconnected') {
        return;
      }
      // prikazivanje toastr-a
      console.log('Ovo nam je iz socketa stiglo', ev.data);
      this.toastr.show('New alarm with id: ' + ev.data + ' has been fired!').onTap.subscribe(() => {
        this.router.navigate(['/alarm_fire_details/' + ev.data]);
      });

    };

    this.socket.onopen = () => {
      console.log('Socket opened');
    };
    this.socket.onclose = () => {
      console.log('Socket closed');
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
      console.log('Log Socket opened');
    };
    this.logSocket.onclose = () => {
      console.log('Log Socket closed');
    };
  }


  closeSocket() {
    this.socket.close();
    this.logSocket.close();
  }

}
