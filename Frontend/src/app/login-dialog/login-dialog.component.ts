import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { AuthService } from '../service/auth.service';

@Component({
  selector: 'app-login-dialog',
  template: `
    <body style="--main-bg-color: #313131; --accent-color: #10ddd3; --hover-color: #00828f; --text-color: #fff; background-color: var(--main-bg-color); overflow-y: auto">
      <h1 mat-dialog-title class="dialog-title">Login</h1>
      <mat-dialog-content class="dialog-content">
      <button mat-icon-button class="close-button" (click)="closeDialog()">
        <mat-icon>close</mat-icon>
      </button>
      <div *ngIf="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
        <mat-form-field appearance="fill">
          <mat-label>E-Mail</mat-label>
          <input matInput type="email" [(ngModel)]="email">
        </mat-form-field>
        <mat-form-field appearance="fill">
          <mat-label>Password</mat-label>
          <input matInput type="password" [(ngModel)]="password">
        </mat-form-field>
        <button mat-button class="login-button" (click)="login()">Login</button>
      </mat-dialog-content>
    </body>
  `,
  styles: [`
    :host {
      --main-bg-color: #313131;
      --accent-color: #10ddd3;
      --hover-color: #00828f;
      --text-color: #fff;
    }

    .dialog-title{
      background-color: var(--main-bg-color);
      text-align: center;
    }

    .dialog-content {
      background-color: var(--main-bg-color);
      text-align: center;
      width: 400px;
    }

    .dialog-title {
      font-size: 24px;
      color: var(--accent-color);
      margin-bottom: 20px;
    }

    .error-message {
      font-size: 16px;
      color: red;
      margin: 15px;
    }

    .dialog-message {
      font-size: 16px;
      color: var(--text-color);
    }

    mat-dialog-content {
      display: flex;
      flex-direction: column;
    }

    .mat-form-field {
      margin-bottom: 20px;
    }

    .close-button {
      position: absolute;
      top: 10px;
      right: 10px;
      color: white; /* oder die Farbe Ihrer Wahl */
    }

    .login-button {
      background-color: var(--accent-color);
      color: var(--text-color);
      font-size: 18px;
      text-transform: capitalize;
      padding: 10px 20px;
      margin: 10px;
      margin-top: 20px;
      cursor: pointer;
      transition: background-color 0.3s ease-in-out;
    }

    .login-button:hover {
      background-color: var(--hover-color);
    }
  `]
})
export class LoginDialogComponent {
  email: string = '';
  password: string = '';
  errorMessage: string = '';
  loading: boolean = false;

  constructor(private authService: AuthService, private dialogRef: MatDialogRef<LoginDialogComponent>) {
    dialogRef.disableClose = true;
  }
  closeDialog() {
    this.dialogRef.close();
  }

  login() {
    this.loading = true;
    this.authService.login(this.email, this.password).subscribe(
      response => {

        this.loading = false;
        if (response.success) {
          this.dialogRef.close({ email: this.email });
        } else {
          this.errorMessage = 'Login data not correct.';
        }
      },
      error => {
        this.loading = false;
        this.errorMessage = 'An error has occurred. Please try again later.';
      }
    );
  }
}
