import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { AuthService } from '../service/auth.service';

@Component({
  selector: 'app-signup-dialog',
  templateUrl: './signup-dialog.component.html',
  styleUrls: ['./signup-dialog.component.css']
})
export class SignupDialogComponent {
  email: string = '';
  password: string = '';
  confirmpassword: string = '';
  first_name: string = '';
  family_name: string = '';
  location: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService, private dialogRef: MatDialogRef<SignupDialogComponent>) {
    dialogRef.disableClose = true;
  }

  closeDialog() {
    this.dialogRef.close();
  }

  signup() {
    if (this.password !== this.confirmpassword) {
      this.errorMessage = "Passwords do not match.";
      return;
    }
    if (!this.email || !this.password || !this.location) {
      this.errorMessage = "Required field missing";
      return;
    }
  
    // Send data to the backend if validation is successful
    this.authService.signup(this.first_name, this.family_name, this.email, this.password, this.location)
      .subscribe({
        next: (response) => {
          // Handle successful signup
          this.performLogin(this.email, this.password);
        },
        error: (errorMessage) => {
          this.errorMessage = errorMessage;
          }
        }
    );
  }

  performLogin(email: string, password: string) {
    this.authService.login(email, password).subscribe({
      next: (response) => {
        if (response.success) {
          this.dialogRef.close({ signupSuccess: true, email: email});
        } else {
          this.errorMessage = 'Login failed.';
        }
      },
      error: (error) => {
        this.errorMessage = 'An error occurred during login.';
      }
    });
  }
}