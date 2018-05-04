import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LogService } from '../../services/log.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  logs;

  constructor(private route: ActivatedRoute, private logService: LogService, private router: Router) {
    this.logs;
  }

  ngOnInit() {

    this.route.queryParams.subscribe((params) => {
      let query = params['query'];
      this.logs = []
      this.logService.logSearch(query).subscribe((data) => {
        console.log(data)
        this.logs = data;
      });
    })
  }

}
