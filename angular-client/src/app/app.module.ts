import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { NotFoundPageComponent } from './components/not-found-page/not-found-page.component';
import { AuthenticationComponent } from './components/authentication/authentication.component';
import { HomepageComponent } from './components/homepage/homepage.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { SearchComponent } from './components/search/search.component';
import { LogService } from './services/log.service';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { TokenInterceptorService } from './services/token-interceptor.service';
import { AuthenticationService } from './services/authentication/authentication.service';
import { ToastrModule } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgxPermissionsModule } from 'ngx-permissions';
import { OnlyLoggedInGuardGuard } from './guards/only-logged-in.guard';
import { AlreadyLoggedInGuard } from './guards/already-logged-in.guard';
import { ChangePasswordComponent } from './components/change-password/change-password.component';
import { AlarmsComponent } from './components/alarms/alarms.component';
import { AlarmsService } from './services/alarms/alarms.service';
import { LogReportComponent } from './components/log-report/log-report.component';
import { AlarmReportComponent } from './components/alarm-report/alarm-report.component';
import { CustomReportComponent } from './components/custom-report/custom-report.component';
import { DlDateTimePickerDateModule } from 'angular-bootstrap-datetimepicker';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { ReportComponent } from './components/report/report.component';
import {AlarmFireSocketService} from './services/socket/alarm-fire-socket.service';
import { AlarmFireDetailsComponent } from './components/alarm-fire-details/alarm-fire-details.component';
import { ConsoleComponent } from './components/console/console/console.component';
import {SharedLogService} from './services/shared-log/shared-log.service';
import { SelectDropDownModule } from 'ngx-select-dropdown';
import { AlarmConsoleComponent } from './components/console/alarm-console/alarm-console.component';

const appRoutes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  { path: 'login', component: AuthenticationComponent, canActivate: [AlreadyLoggedInGuard] },
  { path: 'home', component: HomepageComponent, canActivate: [OnlyLoggedInGuardGuard] },
  { path: 'search', component: SearchComponent, canActivate: [OnlyLoggedInGuardGuard] },
  { path: 'change_password', component: ChangePasswordComponent, canActivate: [OnlyLoggedInGuardGuard] },
  { path: 'alarms', component: AlarmsComponent, canActivate: [OnlyLoggedInGuardGuard] },
  { path: 'reports', component: ReportComponent, canActivate: [OnlyLoggedInGuardGuard]},
  { path: 'log_report', component: LogReportComponent, canActivate: [OnlyLoggedInGuardGuard] },
  { path: 'alarm_report', component: AlarmReportComponent, canActivate: [OnlyLoggedInGuardGuard] },
  { path: 'custom_report', component: CustomReportComponent, canActivate: [OnlyLoggedInGuardGuard] },
  { path: 'alarm_fire_details/:id', component: AlarmFireDetailsComponent, canActivate: [OnlyLoggedInGuardGuard] },
  { path: '**', component: NotFoundPageComponent }

];

@NgModule({
  declarations: [
    AppComponent,
    NotFoundPageComponent,
    AuthenticationComponent,
    HomepageComponent,
    NavbarComponent,
    SearchComponent,
    ChangePasswordComponent,
    AlarmsComponent,
    LogReportComponent,
    AlarmReportComponent,
    CustomReportComponent,
    ReportComponent,
    AlarmFireDetailsComponent,
    ConsoleComponent,
    AlarmConsoleComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    RouterModule.forRoot(
      appRoutes,
    ),
    ToastrModule.forRoot(),
    NgxPermissionsModule.forRoot(),
    HttpClientModule,
    DlDateTimePickerDateModule,
    SelectDropDownModule,
  ],
  providers: [
    LogService,
    TokenInterceptorService,
    AuthenticationService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: TokenInterceptorService,
      multi: true
    },
    AlarmsService,
    OnlyLoggedInGuardGuard,
    AlreadyLoggedInGuard,
    AlarmFireSocketService,
    SharedLogService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
