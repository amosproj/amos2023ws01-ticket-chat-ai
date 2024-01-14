import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-request-type-dialog',
  template: `
    <body style="--main-bg-color: #313131; --accent-color: #10ddd3; --hover-color: #00828f; --text-color: #fff; background-color: var(--main-bg-color); overflow-y: auto">
      <h1 mat-dialog-title class="dialog-title">Please choose a request type</h1>
      <mat-dialog-content class="dialog-content">
        <p class="dialog-message">We couldn't automatically detect the request type from your message. Please select the appropriate request type:</p>
        <button mat-button class="request-type-button" (click)="selectType('Incident')">Incident</button>
        <button mat-button class="request-type-button" (click)="selectType('Service Request')">Service Request</button>
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

    .dialog-title, .dialog-content {
      background-color: var(--main-bg-color);
      text-align: center;
    }

    .dialog-title {
      font-size: 24px;
      color: var(--accent-color);
      margin-bottom: 20px;
    }

    .dialog-message {
      font-size: 16px;
      color: var(--text-color);
    }

    .request-type-button {
      background-color: var(--accent-color);
      color: var(--text-color);
      font-size: 18px;
      text-transform: capitalize;
      padding: 10px 20px;
      margin: 10px;
      cursor: pointer;
      transition: background-color 0.3s ease-in-out;
    }

    .request-type-button:hover {
      background-color: var(--hover-color);
    }
  `]
})
export class RequestTypeDialogComponent {
  constructor(private dialogRef: MatDialogRef<RequestTypeDialogComponent>) {
    dialogRef.disableClose = true;
  }

  selectType(type: string) {
    this.dialogRef.close(type);
  }
}
