import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'app';
  consoleBtn = false;
  alarmConsoleBtn = false;


  ngOnInit(){
  }

  toggleConsoleButton(){
    this.alarmConsoleBtn = false;
    this.consoleBtn = !this.consoleBtn;
  }

  toggleAlarmConsoleButton(){
    this.consoleBtn = false;
    this.alarmConsoleBtn = !this.alarmConsoleBtn;
  }

  hideConsole(){
    this.consoleBtn = false;
    this.alarmConsoleBtn = false;
  }
}
