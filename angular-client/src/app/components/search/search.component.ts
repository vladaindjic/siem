import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LogService } from '../../services/log.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  logovi;

  constructor(private route: ActivatedRoute, private logService: LogService, private router: Router) {
    this.logovi;
  }

  ngOnInit() {

    this.route.queryParams.subscribe((params) => {
      let query = params['query'];
      this.logService.logSearch(query).subscribe((data) => {
        console.log(data)
        this.logovi = data;
        this.logovi = JSON.parse(this.logovi)
      });
    })
  }

}
