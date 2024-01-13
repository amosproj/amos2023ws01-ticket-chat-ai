import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-request-type-dialog',
  template: `
    <h1 mat-dialog-title>Please choose a request type</h1>
    <mat-dialog-content>
      <p>We couldn't automatically detect the request type from your message. Please select the appropriate request type:</p>
      <button mat-button (click)="selectType('issue')">Report an Issue</button>
      <button mat-button (click)="selectType('service')">Service Request</button>
    </mat-dialog-content>
  `,
  styles: [/* CSS styles here */]
})
export class RequestTypeDialogComponent {
  constructor(private dialogRef: MatDialogRef<RequestTypeDialogComponent>) {}

  selectType(type: string) {
    this.dialogRef.close(type);
  }
}
