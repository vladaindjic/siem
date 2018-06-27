import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {AlarmsService} from '../../services/alarms/alarms.service';

@Component({
  selector: 'app-alarm-fire-details',
  templateUrl: './alarm-fire-details.component.html',
  styleUrls: ['./alarm-fire-details.component.css']
})
export class AlarmFireDetailsComponent implements OnInit {

  public alarmFire: Object = null;

  constructor(private route: ActivatedRoute,
              private alarmService: AlarmsService) { }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let id: string = params['id'];
      this.alarmService.getAlarmFireDetails(id).subscribe(af => {
        this.alarmFire = JSON.parse(af as string);
        console.log(this.alarmFire)
      });
    });
  }

}
