import { Component } from '@angular/core';
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

  constructor(private ticketService: TicketService, private logger: LogService) {}

  handleSend(value: string) {
    if (value) {
      // push user message to chat
      this.chatMessages.push({ messageText: value, isUser: true });
      this.logger.log('Trying to send message to backend server: ' + value)

      // send message to server and handle response
      this.ticketService.send(value).subscribe(
        (response: any) => {
          const messageText = JSON.stringify(response) // use "text" as per the backend API
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
