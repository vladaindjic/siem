import { Component, OnInit } from '@angular/core';

import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgxPermissionsService } from 'ngx-permissions';
import { ToastrService } from 'ngx-toastr';
import { AuthenticationService } from '../../services/authentication/authentication.service';
import { LoggedUtils } from '../../utils/logged-utils';
import { IUser } from '../../model/IUser';


@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.css'],
  providers: [AuthenticationService]
})
export class AuthenticationComponent implements OnInit {

  loginForm;
  private username: string;
  private password: string;

  constructor(private autheticationService: AuthenticationService, private permissionsService: NgxPermissionsService,
    private router: Router, private toastr: ToastrService) {
    this.username = '';
    this.password = '';
  }

  ngOnInit() {
    this.loginForm = new FormGroup({
      username: new FormControl('', Validators.compose([Validators.required, Validators.minLength(3)])),
      password: new FormControl('', Validators.compose([Validators.required, Validators.minLength(3)]))
    });
  }

  authenticate() {
    const credentials: IUser = this.loginForm.value;
    this.autheticationService.authenticateUser(credentials).subscribe(
      data => {
        console.log(JSON.stringify(data))
        localStorage.setItem('loggedUser', JSON.stringify(data)),
          this.router.navigate(['/home']);

        const perm = [];
        perm.push(LoggedUtils.getRole());
        this.permissionsService.loadPermissions(perm);
        this.permissionsService.permissions$.subscribe((item) => {
        });
        this.toastr.success('You are loged in', 'Welcome!');
      },
      error => this.toastr.error('Incorrect username and/or password'),
      () => console.log(JSON.parse(localStorage.getItem('loggedUser')))
    );
  }

}