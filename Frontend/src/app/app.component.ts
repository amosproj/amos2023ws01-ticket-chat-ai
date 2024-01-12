import { Component, OnInit, ViewChild, ElementRef, ChangeDetectorRef } from '@angular/core';
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
  files: any[] = [];
  waitingServerResponse: boolean = false;
  recognition: any;
  errorMessage: string = '';
  recordingState: 'idle' | 'recording' = 'idle';
  recognitionTimeout: any;
  selectedRequestType: string = '';

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

  chooseRequestType(requestType: string) {
    this.selectedRequestType = requestType;
    const thankYouMessage = `Vielen Dank! Ich habe Dein Ticket erfolgreich angelegt. [dead link behind ticket] RequestType: ${requestType}`;
    this.chatMessages.push({ messageText: thankYouMessage, isUser: false, files: [] });
    this.clearFiles();
    this.waitingServerResponse = false;
  }

  sendAttachmentsToServer(response: any) {
    this.ticketService.sendFiles(this.files, response.id).subscribe(
      (attachmentsResponse: any) => {
        const messageText = JSON.stringify(attachmentsResponse);
        this.chatMessages.push({ messageText, isUser: false, files: [] });
        this.clearFiles();

        this.logger.log('Attachments were sent successfully: ' + attachmentsResponse);
        this.waitingServerResponse = false;
      },
      (error: any) => {
        this.handleError('Leider ist ein Fehler aufgetreten. Versuche es erneut oder später noch einmal, wir bitten um Entschuldigung');
      }
    );
  }

  handleSend(value: string, emailInput: string) {
    this.errorMessage = "";
    if (!value) {
      this.errorMessage = 'Bitte verfasse eine Nachricht oder hinterlasse eine Sprachnachricht.';
      return;
    }

    this.chatMessages.push({ messageText: value, isUser: true, files: this.files });
    this.logger.log('Trying to send message to backend server: ' + value);

    this.ticketService.send(value, emailInput).subscribe(
      (response: any) => {
        let messageText = '';

        if (typeof response === 'object') {
          messageText = JSON.stringify(response);
        } else {
          messageText = response;
        }

        this.changeDetector.detectChanges();

        if (this.files.length !== 0) {
          this.sendAttachmentsToServer(response);
        } else {
          this.chatMessages.push({ messageText, isUser: false, files: [] });
        }

        this.logger.log('Received response from backend server: ' + response);
        this.waitingServerResponse = false;
      },
      (error) => {
        this.handleError('Leider ist ein Fehler aufgetreten. Versuche es erneut oder später noch einmal, wir bitten um Entschuldigung');
      }
    );

    this.chatInput = "";
    this.waitingServerResponse = true;
  }

  startSpeechRecognition() {
    if (this.recordingState === 'idle') {
      this.startRecording();
    } else {
      this.stopRecording();
    }
  }

  startRecording() {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      this.recognition = new ((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition)();
      this.recognition.lang = 'de-DE';
      this.recognition.interimResults = false;
      this.recognition.maxAlternatives = 1;
      this.recognition.continuous = true;

      this.recognition.start();

      this.recognition.onresult = (event: any) => {
        this.chatInput = "";
        for (let i = 0; i < event.results.length; i++) {
          this.chatInput += event.results[i][0].transcript;
        }
        this.resetRecognitionTimeout();
      };

      this.recognition.onerror = (event: any) => {
        this.handleError('Leider ist ein Fehler aufgetreten. Versuche es erneut oder später noch einmal, wir bitten um Entschuldigung');
      };

      this.recordingState = 'recording';
      this.setRecognitionTimeout();
    } else {
      this.handleError('Speech Recognition API is not supported in this browser. Try using Chrome or Edge');
    }
  }

  stopRecording() {
    this.recognition.stop();
    clearTimeout(this.recognitionTimeout);
    this.recordingState = 'idle';
  }

  setRecognitionTimeout() {
    this.recognitionTimeout = setTimeout(() => {
      if (this.recordingState === 'recording') {
        this.stopRecording();
        this.handleError('Voice input stopped due to inactivity.');
      }
    }, 30000);
  }

  resetRecognitionTimeout() {
    clearTimeout(this.recognitionTimeout);
    if (this.recordingState === 'recording') {
      this.setRecognitionTimeout();
    }
  }

  handleError(errorMessage: string) {
    this.errorMessage = errorMessage;
    this.logger.error(errorMessage);
  }
}
