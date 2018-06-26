import {ToastrService} from 'ngx-toastr';
import {Router} from '@angular/router';

export class AlarmFireSocketClass {
  socketUrl: string;
  socket: WebSocket;
  toastr: ToastrService;
  router: Router;

  constructor(socketUrl: string, toastr: ToastrService, router: Router) {
    this.socketUrl = socketUrl;
    this.openSocket();
    this.toastr = toastr;
    this.router = router;
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

  closeSocket() {
    this.socket.close();
  }

}
