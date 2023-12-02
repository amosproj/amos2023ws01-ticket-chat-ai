import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { TicketService } from './service/ticket.service';
import { LogService } from './service/logging.service';

interface ChatMessages {
  messageText: string;
  isUser: boolean;
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
  files!: any[];

  @ViewChild("fileDropRef", { static: true }) fileDropEl!: ElementRef;

  constructor(private ticketService: TicketService, private logger: LogService) {
    this.droppedFiles = [];
  }

  ngOnInit() {

  }

  getFiles(event: any){
    this.files = event;
  }

  handleSend(value: string, emailInput: string) {

    if (value) {
      // push user message to chat
      this.chatMessages.push({ messageText: value, isUser: true });
      this.logger.log('Trying to send message to backend server: ' + value)

      // send message to server and handle response
      this.ticketService.send(value, this.emailInput).subscribe(
        (response: any) => {
          const messageText = JSON.stringify(response) // use "text" as per the backend API
          this.chatMessages.push({ messageText, isUser: false }); // push server message to chat

          if(this.files){
            this.ticketService.sendFiles(this.files, response.id);
            // clear files
          }

          this.logger.log('Received response from backend server: ' + response);
        },
        // push error message to chat
        (error) => {
          this.logger.log('Error sending message:' + error);
          this.chatMessages.push({ messageText: 'Error sending message.....', isUser: false });
        }
      );

      // clear the chat input
      this.chatInput = "";
    }
  }
}


