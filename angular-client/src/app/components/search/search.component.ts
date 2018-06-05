import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LogService } from '../../services/log.service';
import {ILog} from "../../model/ILog";
import {IFindLogsResult} from "../../model/IFindLogsResult";

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  logs: ILog[];
  count: number;

  constructor(private route: ActivatedRoute, private logService: LogService, private router: Router) {
    this.logs = [];
    this.count = 0;
  }

  ngOnInit() {

    this.route.queryParams.subscribe((params) => {
      let query = params['query'];
      this.logService.logSearch(query).subscribe((data) => {
        let res: IFindLogsResult = JSON.parse(data as string) as IFindLogsResult;
        this.count = res.count;
        this.logs = res.logs;
        console.log(this.count)
      });
    })
  }

}
