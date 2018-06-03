import { Component, OnInit } from '@angular/core';
import { LoggedUtils } from '../../utils/logged-utils';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {

  constructor() { }

  ngOnInit() {
    
  }


  btnclicked(){
    console.log(LoggedUtils.getRole());
  }
}
