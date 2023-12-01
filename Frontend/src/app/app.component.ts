import { Component, ChangeDetectorRef } from '@angular/core';
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
export class AppComponent {
  title: string = "TalkTix";
  chatInput: string = "";
  chatMessages: ChatMessages[] = [];
  recognition: any;

  constructor(private ticketService: TicketService, private logger: LogService, private changeDetector: ChangeDetectorRef) {}

  handleSend(value: string) {
    if (value) {
      this.chatMessages.push({ messageText: value, isUser: true });
      this.sendMessageToBackend(value);
      this.chatInput = "";
    }
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
        this.logger.error('Recognition Error:' + event.error);
      };

      this.recognition.start();
    } else {
      this.logger.error('Speech Recognition API is not supported in this browser.');
    }
  }

  sendMessageToBackend(message: string) {
    this.ticketService.send(message).subscribe(
      (response: any) => {
        const messageText = response.text;
        this.chatMessages.push({ messageText, isUser: false });
        this.logger.log('Received response from backend server: ' + response);
        this.changeDetector.detectChanges();
      },
      (error) => {
        this.logger.error('Error sending message:' + error);
        this.chatMessages.push({ messageText: 'Error sending message.....', isUser: false });
      }
    );
  }
}
