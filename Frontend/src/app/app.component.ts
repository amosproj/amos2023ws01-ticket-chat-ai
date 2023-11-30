import { Component, OnInit } from '@angular/core';
import { TicketService } from './service/ticket.service';
import { LogService } from './service/logging.service';

interface ChatMessages {
  messageText: string;
  isUser: boolean;
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
  droppedFiles: File[] | null;

  constructor(private ticketService: TicketService, private logger: LogService) {
    this.droppedFiles = [];
  }

  ngOnInit() {
    this.setupDragAndDrop();
  }

  setupDragAndDrop() {
    let dropArea = document.getElementById('drop-area');
  
    if (!dropArea) {
      console.error("Element with ID 'drop-area' not found");
      return;
    }
  
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dropArea?.addEventListener(eventName, (e) => this.preventDefaults(e), false);
    });
  
    ['dragenter', 'dragover'].forEach(eventName => {
      dropArea?.addEventListener(eventName, (e) => this.highlight(e), false);
    });
  
    ['dragleave', 'drop'].forEach(eventName => {
      dropArea?.addEventListener(eventName, (e) => this.unhighlight(e), false);
    });
  }

  preventDefaults(e: Event) {
    e.preventDefault();
    e.stopPropagation();
  }

  highlight(e: Event) {
    let dropArea = document.getElementById('drop-area');
    if (!dropArea) {
      console.error("Element with ID 'drop-area' not found");
      return;
    }
    dropArea.classList.add('highlight');
  }

  unhighlight(e: Event) {
    let dropArea = document.getElementById('drop-area');
    if (!dropArea) {
      console.error("Element with ID 'drop-area' not found");
      return;
    }
    dropArea.classList.remove('highlight');
  }

  handleDrop(e: DragEvent) {
    let dt = e.dataTransfer;
    if (dt) {
      this.droppedFiles = Array.from(dt.files);
    }
  }

  handleFiles(files: FileList) {
    Array.from(files).forEach(file => this.uploadFile(file));
  }

  uploadFile(file: File) {
    let url = 'YOUR URL HERE'; // Replace with your URL
    let formData = new FormData();

    formData.append('file', file);

    fetch(url, {
      method: 'POST',
      body: formData
    })
    .then(() => { /* Done. Inform the user */ })
    .catch(() => { /* Error. Inform the user */ });
  }

  handleSend(value: string) {
    // Upload dropped files
    if (this.droppedFiles) {
      this.droppedFiles.forEach(file => this.uploadFile(file));
      this.droppedFiles = null; // Clear the files after uploading
    }

    if (value) {
      // push user message to chat
      this.chatMessages.push({ messageText: value, isUser: true });
      this.logger.log('Trying to send message to backend server: ' + value)

      // send message to server and handle response
      this.ticketService.send(value, this.emailInput).subscribe(
        (response: any) => {
          const messageText = response.text; // use "text" as per the backend API
          this.chatMessages.push({ messageText, isUser: false }); // push server message to chat

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
