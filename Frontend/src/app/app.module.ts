import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from "@angular/material/button";
import { MatInputModule } from "@angular/material/input";
import { MatIconModule } from '@angular/material/icon';
import { DragAndDropModule } from './drag-and-drop/drag-and-drop.module';
import { MatCardModule } from '@angular/material/card';
import { MatDialogModule } from '@angular/material/dialog';
import { RequestTypeDialogComponent } from './request-type-dialog/request-type-dialog.component';
import { LoginDialogComponent } from './login-dialog/login-dialog.component';
import { SignupDialogComponent } from './signup-dialog/signup-dialog.component';
import { EditDialogComponent } from './edit-dialog/edit-dialog.component';
import {SessionExpiredDialogComponent} from './session-expired-dialog/session-expired-dialog.component';
import { MatSelectModule } from '@angular/material/select';
import { TicketFormComponent } from './ticket-form/ticket-form.component';
import {MatChipsModule} from "@angular/material/chips";
import { LogoutDialogComponent } from './logout-dialog/logout-dialog.component';

@NgModule({
  declarations: [
    AppComponent,
    RequestTypeDialogComponent,
    LoginDialogComponent,
    SignupDialogComponent,
    TicketFormComponent,
    EditDialogComponent,
    SessionExpiredDialogComponent,
    LogoutDialogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    NoopAnimationsModule,
    MatButtonModule,
    DragAndDropModule,
    MatCardModule,
    MatDialogModule,
    MatInputModule,
    MatIconModule,
    MatSelectModule,
    ReactiveFormsModule,
    MatChipsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
