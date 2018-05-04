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
import { HttpClientModule } from '@angular/common/http';
import { TokenInterceptorService } from './services/token-interceptor.service';

const appRoutes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  { path: 'login', component: AuthenticationComponent },
  { path: 'home', component: HomepageComponent },
  { path: 'search', component: SearchComponent },
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
  ],
  imports: [
    BrowserModule,
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    RouterModule.forRoot(
      appRoutes,
    ),
    HttpClientModule
  ],
  providers: [
    LogService,
    TokenInterceptorService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
