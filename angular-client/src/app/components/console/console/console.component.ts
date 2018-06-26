import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-console',
  templateUrl: './console.component.html',
  styleUrls: ['./console.component.css']
})
export class ConsoleComponent implements OnInit {

  listaLogova: any[] = [];
  constructor() { }

  ngOnInit() {
    let string = "RADIM KAKO TREBA";
    this.lalala(string);
  }

  lalala(string){
    for (let index = 0; index < 50; index++) {
      this.listaLogova.push(string);
    }
  }

  clearConsole(){
    this.listaLogova = [];
  }

}
