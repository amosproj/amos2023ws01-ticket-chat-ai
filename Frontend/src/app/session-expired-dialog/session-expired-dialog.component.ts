import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-session-expired-dialog',
  template: `
    <body style="--main-bg-color: #313131; --accent-color: #10ddd3; --hover-color: #00828f; --text-color: #fff; background-color: var(--main-bg-color); overflow-y: auto">
      <div class="shared-dialog-styles">
        <div class="shared-dialog-container">
          <ng-container mat-dialog-content class="shared-dialog-content">
            <div [innerHTML]="message"></div>
          </ng-container>
          <ng-container mat-dialog-actions class="shared-dialog-actions">
            <button mat-button class="ok-button" (click)="closeDialog()">OK</button>
          </ng-container>
        </div>
      </div>
    </body>
  `,
  styleUrls: ['./session-expired-dialog.component.css']
})
export class SessionExpiredDialogComponent {
  message: string = 'Your session has expired. <br />Please login again.';

  constructor(private dialogRef: MatDialogRef<SessionExpiredDialogComponent>) {}

  closeDialog(): void {
    this.dialogRef.close();
  }
}
