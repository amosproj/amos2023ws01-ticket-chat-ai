import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'logout-dialog',
  templateUrl: './logout-dialog.component.html',
  styleUrls: ['./logout-dialog.component.css']
})
export class LogoutDialogComponent {

  constructor(private dialogRef: MatDialogRef<LogoutDialogComponent>) {}

  closeDialog(): void {
    this.dialogRef.close();
  }
}
