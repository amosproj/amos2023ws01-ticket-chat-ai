import {Component} from '@angular/core';
import {MatDialogRef} from '@angular/material/dialog';
import {AuthService} from '../service/auth.service';

@Component({
  selector: 'app-login-dialog',
  templateUrl: './login-dialog.component.html',
  styleUrls: ['./login-dialog.component.css']
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
          this.dialogRef.close({loginSuccess: true, email: this.email });
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
