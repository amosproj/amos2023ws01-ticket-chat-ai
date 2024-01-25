import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { AuthService } from '../service/auth.service';

@Component({
  selector: 'app-edit-dialog',
  templateUrl: './edit-dialog.component.html',
  styleUrls: ['./edit-dialog.component.css']
})
export class EditDialogComponent {
  old_email: string = '';
  old_password: string = '';
  email: string = '';
  password: string = '';
  confirmpassword: string = '';
  firstname: string = '';
  lastname:string = '';
  officeLocation: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService, private dialogRef: MatDialogRef<EditDialogComponent>) {
    dialogRef.disableClose = true;
  }

  closeDialog() {
    this.dialogRef.close();
  }

  edit() {
    if (this.password !== this.confirmpassword) {
      this.errorMessage = "New passwords do not match.";
      return;
    }
    if (!this.email || !this.old_password || !this.officeLocation) {
      this.errorMessage = "Required field missing";
      return;
    }
    if (!this.password) {
      this.password = this.old_password
    }

    // Send data to the backend if validation is successful
    this.authService.edit(this.old_email, this.old_password, this.firstname, this.lastname, this.email, this.password, this.officeLocation)
      .subscribe({
        next: (response) => {
          this.dialogRef.close({ editSuccess: true, email: this.email, password: this.password});
        },
        error: (errorMessage) => {
          this.errorMessage = errorMessage;
          }
        }
    );
  }
}
