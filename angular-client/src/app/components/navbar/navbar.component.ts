import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
//import { ToastrService } from 'ngx-toastr';
//import { NgxPermissionsService } from 'ngx-permissions';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { LoggedUtils } from '../../utils/logged-utils';
import { NgxPermission } from 'ngx-permissions/model/permission.model';
import { NgxPermissionsService } from 'ngx-permissions';
import { ToastrService } from 'ngx-toastr';
import {LogService} from "../../services/log.service";
import {AlarmFireSocketService} from '../../services/socket/alarm-fire-socket.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  private perm;
  searchForm: FormGroup;

  constructor(private router: Router, private fb: FormBuilder,
    private permissionsService: NgxPermissionsService, private toastr: ToastrService,
              private searchService: LogService, private route: ActivatedRoute,
              private alarmFireSocketService: AlarmFireSocketService) {
  }

  ngOnInit() {
    const perm = [];
    perm.push(LoggedUtils.getRole());
    this.permissionsService.loadPermissions(perm);
    this.permissionsService.permissions$.subscribe((permisios) => {
    });

    this.searchForm = this.fb.group({
      query: new FormControl('', [Validators.required])
    }, { updateOn: 'submit' });

    this.readQueryFromURL();
  }
  private readQueryFromURL(){

    this.route.queryParams.subscribe((params) => {
      let query = params['query'];
      this.searchService.setQuery(query);
      this.searchForm.controls['query'].setValue(query);
    })

  }

  search() {
    let query = this.searchForm.value.query;
    this.searchService.setQuery(query);
    this.router.navigate(['/search'], { queryParams: { query: query } });
  }

  logout() {
    this.alarmFireSocketService.closeSocket(LoggedUtils.getUsername());
    LoggedUtils.clearLocalStorage();
    this.router.navigate(['/login']);
    this.toastr.success('You are loged out!');
    this.permissionsService.flushPermissions();
  }

}
