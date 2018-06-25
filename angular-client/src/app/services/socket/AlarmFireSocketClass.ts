import {ToastrService} from 'ngx-toastr';

export class AlarmFireSocketClass {
  socketUrl: string;
  socket: WebSocket;
  toastr: ToastrService;

  constructor(socketUrl: string, toastr: ToastrService) {
    this.socketUrl = socketUrl;
    this.openSocket();
    this.toastr = toastr;
  }

  openSocket() {
    this.socket = new WebSocket(this.socketUrl);

    this.socket.onmessage = ev => {
      console.log('Ovo nam je iz socketa stiglo', ev.data);
      this.toastr.show('Alarm fired!');
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
