import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
//import { ToastrService } from 'ngx-toastr';
//import { NgxPermissionsService } from 'ngx-permissions';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  private perm;
  searchForm: FormGroup;

  constructor(private router: Router, private fb: FormBuilder) {
  }

  ngOnInit() {
   /* const perm = [];
    perm.push(LoggedUtils.getRole());
    this.permissionsService.loadPermissions(perm);
    this.permissionsService.permissions$.subscribe((permisios) => {
    });
    */
    this.searchForm=this.fb.group({
      query: new FormControl('', [Validators.required])
    }, { updateOn: 'submit' });
  }

  logout() {
    console.log("Logout")/*
    LoggedUtils.clearLocalStorage();
    this.router.navigate(['/login']);
    this.toastr.success('You are loged out!');
    this.permissionsService.flushPermissions();*/
  }


  search() {
    console.log("Search")
    let query = this.searchForm.value.query;
    this.router.navigate(['/search'],{ queryParams: {query:query}});
  }

}
