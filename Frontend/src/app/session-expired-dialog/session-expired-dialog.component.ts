import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-session-expired-dialog',
  templateUrl: './session-expired-dialog.component.html',
  styleUrls: ['./session-expired-dialog.component.css']
})
export class SessionExpiredDialogComponent {

  constructor(private dialogRef: MatDialogRef<SessionExpiredDialogComponent>) {}

  closeDialog(): void {
    this.dialogRef.close();
  }
}
