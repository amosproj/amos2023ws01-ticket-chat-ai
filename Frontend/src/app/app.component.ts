import { Component, OnInit, ViewChild, ElementRef, ChangeDetectorRef } from '@angular/core';
import { TicketService } from './service/ticket.service';
import { LogService } from './service/logging.service';
import { DragAndDropComponent } from './drag-and-drop/drag-and-drop.component';
import { throwError } from 'rxjs';

interface ChatMessages {
  messageText: string;
  isUser: boolean;
  files: any[];
}

// Class definition for file with progress
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
  files: any[] = [];
  waitingServerResponse: boolean = false;
  recognition: any;
  errorMessage: string = ''; // New property for error messages

  @ViewChild("fileDropRef", { static: true }) fileDropEl!: ElementRef;
  @ViewChild(DragAndDropComponent) dragAndDropComponent!: DragAndDropComponent;

  constructor(private ticketService: TicketService, private logger: LogService, private changeDetector: ChangeDetectorRef) {}

  ngOnInit() {}

  getFiles(event: any) {
    this.files = event;
  }

  formatBytes(bytes: any, decimals = 2) {
    if (bytes === 0) {
      return "0 Bytes";
    }
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  }

  clearFiles() {
    this.dragAndDropComponent.clearFiles();
    this.files = [];
  }

  sendAttachmentsToServer(response: any) {
    // send attachments to server and handle response
    this.ticketService.sendFiles(this.files, response.id).subscribe(
      (attachmentsResponse: any) => {
        const messageText = JSON.stringify(attachmentsResponse);
        this.chatMessages.push({ messageText, isUser: false, files: [] });
        this.clearFiles();

        this.logger.log('Attachments were sent successfully: ' + attachmentsResponse);
        this.waitingServerResponse = false;
      },
      (error: any) => {
        this.errorMessage = 'Leider ist ein Fehler aufgetreten. Versuche es erneut oder später noch einmal, wir bitten um Entschuldigung';
        this.logger.error('Error when sending Attachments: ' + error);
        this.chatMessages.push({ messageText: 'Error sending Attachments.....', isUser: false, files: [] });
        this.waitingServerResponse = false;
      }
    );
  }

  handleSend(value: string, emailInput: string) {
    this.errorMessage = "";
    if (!value && !emailInput) {
      this.errorMessage = 'Bitte verfasse eine Nachricht oder hinterlasse eine Sprachnachricht.';
      return; // Stop further execution if no input message is provided
    }

    this.chatMessages.push({ messageText: value, isUser: true, files: this.files });
    this.logger.log('Trying to send message to backend server: ' + value);

    // send message to server and handle response
    this.ticketService.send(value, emailInput).subscribe(
      (response: any) => {
        let messageText = '';

        if (typeof response === 'object') {
          messageText = JSON.stringify(response); // Convert object to string
        } else {
          messageText = response; // Use response as is
        }

        // Update the view after receiving the server response
        this.changeDetector.detectChanges();

        // if attachments were inputted in UI, send them to backend
        if (this.files.length !== 0) {
          this.sendAttachmentsToServer(response);
        } else {
          this.chatMessages.push({ messageText, isUser: false, files: [] });
        }

        this.logger.log('Received response from backend server: ' + response);
        this.waitingServerResponse = false;
      },
      (error) => {
        this.errorMessage = 'Leider ist ein Fehler aufgetreten. Versuche es erneut oder später noch einmal, wir bitten um Entschuldigung';
        this.logger.error('Error sending message:' + error);
        this.chatMessages.push({ messageText: 'Error sending message.....', isUser: false, files: [] });
        this.waitingServerResponse = false;
      }
    );

    this.chatInput = "";
    this.waitingServerResponse = true;
  }

  startSpeechRecognition() {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      this.recognition = new ((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition)();

      this.recognition.lang = 'de-DE';
      this.recognition.interimResults = false;
      this.recognition.maxAlternatives = 1;

      this.recognition.onresult = (event: any) => {
        this.chatInput = event.results[0][0].transcript;
        this.changeDetector.detectChanges();
      };

      this.recognition.onerror = (event: any) => {
        this.errorMessage = 'Leider ist ein Fehler aufgetreten. Versuche es erneut oder später noch einmal, wir bitten um Entschuldigung';
        this.logger.error('Recognition Error:' + event.error);
      };

      this.recognition.start();
    } else {
      this.errorMessage = 'Speech Recognition API is not supported in this browser. Try using Chrome or Edge';
      this.logger.error('Speech Recognition API is not supported in this browser.');
    }
  }
}
