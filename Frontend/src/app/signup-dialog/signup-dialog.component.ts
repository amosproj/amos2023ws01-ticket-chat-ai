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
  firstname: string = '';
  lastname:string = '';
  officeLocation: string = '';
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
    if (!this.email || !this.password || !this.officeLocation) {
      this.errorMessage = "Required field missing";
      return;
    }
  
    // Send data to the backend if validation is successful
    this.authService.signup(this.firstname, this.lastname, this.email, this.password, this.officeLocation)
      .subscribe({
        next: (response) => {
          // Handle successful signup
          this.dialogRef.close();
        },
        error: (errorMessage) => {
          this.errorMessage = errorMessage;
          }
        }
    );
  } 
}
