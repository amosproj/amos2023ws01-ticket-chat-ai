import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { TicketService } from './service/ticket.service';
import { LogService } from './service/logging.service';
import { DragAndDropComponent } from './drag-and-drop/drag-and-drop.component';

interface ChatMessages {
  messageText: string;
  isUser: boolean;
  files: any[];
}

class FileWithProgress {
  file: File;
  progress: number;

  constructor(file: File) {
    this.file = file;
    this.progress = 0;
  }
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  title: string = "TalkTix";
  chatInput: string = "";
  emailInput: string = "";
  chatMessages: ChatMessages[] = [];
  droppedFiles: FileWithProgress[] | null;
  files: any[] = [];
  waitingServerResponse: boolean = false;

  @ViewChild("fileDropRef", { static: true }) fileDropEl!: ElementRef;

  @ViewChild(DragAndDropComponent) dragAndDropComponent!: DragAndDropComponent;

  constructor(private ticketService: TicketService, private logger: LogService) {
    this.droppedFiles = [];
  }

  ngOnInit() {

  }

  getFiles(event: any) {
    this.files = event;
  }

  formatBytes(bytes: any, decimals = 2) {
    if (bytes === 0) {
      return "0 Bytes";
    }
    const k = 1024;
    const dm = decimals <= 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  }

  clearFiles() {
    this.dragAndDropComponent.clearFiles();
    this.droppedFiles = [];
  }

  sendAttachmentsToServer(response: any) {
    // send attachments to server and handle response
    this.ticketService.sendFiles(this.files, response.id).subscribe(
      (attachmentsResponse: any) => {

        this.clearFiles();

        this.logger.log('Attachments was send successfully: ' + attachmentsResponse);
        console.log('Success:', response);
        this.waitingServerResponse = false;
      },
      (error: any) => {
        this.logger.error('Error when sending Attachments: ' + error);
        this.chatMessages.push({ messageText: 'Error sending Attachments.....', isUser: false, files: [] });
        this.waitingServerResponse = false;
      }
    );
  }

  handleSend(value: string, emailInput: string) {

    if (value) {
      // push user message to chat
      this.chatMessages.push({ messageText: value, isUser: true, files: this.files });
      this.logger.log('Trying to send message to backend server: ' + value)

      // send message to server and handle response
      this.ticketService.send(value, emailInput).subscribe(
        (response: any) => {
          const messageText = JSON.stringify(response)
          this.chatMessages.push({ messageText, isUser: false, files: [] });

          // if attachments was inputed in UI, send them to backend
          if (this.files.length != 0) {
            this.sendAttachmentsToServer(response);
          }

          this.logger.log('Received response from backend server: ' + response);
          this.waitingServerResponse = false;
        },
        // push error message to chat
        (error) => {
          this.logger.log('Error sending message:' + error);
          this.chatMessages.push({ messageText: 'Error sending message.....', isUser: false, files: [] });
          this.waitingServerResponse = false;
        }
      );

      // clear the chat input
      this.chatInput = "";

      // display waiting for server response animation
      this.waitingServerResponse = true;
    }
  }

}


