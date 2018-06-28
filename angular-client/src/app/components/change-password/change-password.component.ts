import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AuthenticationService } from '../../services/authentication/authentication.service';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';
import { LoggedUtils } from '../../utils/logged-utils';
import { NgxPermissionsService } from 'ngx-permissions';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.css']
})
export class ChangePasswordComponent implements OnInit {

  changePasswordForm;
  private old_password: string;
  private new_password: string;
  private repeat_new_password: string;

  constructor(private autheticationService: AuthenticationService, private permissionsService: NgxPermissionsService,
    private router: Router, private toastr: ToastrService, private fb: FormBuilder) {
    this.old_password = '';
    this.new_password = '';
    this.repeat_new_password = '';
  }

  ngOnInit() {
    this.changePasswordForm = this.fb.group({
      old_password: new FormControl('', Validators.compose([Validators.required, Validators.minLength(3)])),
      new_password: new FormControl('', Validators.compose([Validators.required,
      Validators.pattern('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&].{8,}')])),
      repeat_new_password: new FormControl('', Validators.compose([Validators.required, Validators.minLength(3)]))
    }, { validator: [this.validateRepeatPass('new_password', 'repeat_new_password')] });
  }

  changeUserPass() {
    const pass_change = this.changePasswordForm.value;
    this.autheticationService.changeUserPass(pass_change).subscribe(
      data => {
        this.logout();
      },
      error => this.toastr.error('Passord changing failed')
    );
  }

  logout() {
    LoggedUtils.clearLocalStorage();
    this.router.navigate(['/login']);
    this.toastr.success('Successfuly changed password')
    this.toastr.warning('You are loged out!');
    this.permissionsService.flushPermissions();
  }


  validateRepeatPass(new_pass: string, repat_pass: string) {
    return (group: FormGroup): { [key: string]: any } => {
      const checkNew = group.controls[new_pass];
      const checkRepeated = group.controls[repat_pass];
      if (checkNew.value !== checkRepeated.value) {
        return {
          notEqualPass: true
        };
      }
    };
  }
}
