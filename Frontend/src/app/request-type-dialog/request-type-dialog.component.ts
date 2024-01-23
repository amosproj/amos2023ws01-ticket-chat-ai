import {Component} from '@angular/core';
import {MatDialogRef} from '@angular/material/dialog';

@Component({
  selector: 'app-request-type-dialog',
  templateUrl: './request-type-dialog.component.html',
  styleUrls: ['./request-type-dialog.component.css']
})
export class RequestTypeDialogComponent {
  constructor(private dialogRef: MatDialogRef<RequestTypeDialogComponent>) {
    dialogRef.disableClose = true;
  }

  selectType(type: string) {
    this.dialogRef.close(type);
  }
}
