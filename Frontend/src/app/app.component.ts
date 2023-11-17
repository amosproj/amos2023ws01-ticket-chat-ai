import { Component } from '@angular/core';
import { TicketService } from './service/ticket.service';

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

  constructor(private ticketService: TicketService) {}

  handleSend(value: string) {
    if (value) {
      // push user message to chat
      this.chatMessages.push({ messageText: value, isUser: true });

      // send message to server and handle response
      this.ticketService.send(value).subscribe(
        (response: any) => {
          const messageText = response.text; // use "text" as per the backend API
          this.chatMessages.push({ messageText, isUser: false }); // push server message to chat

          console.log(response);
        },
        // push error message to chat
        (error) => {
          console.error('Error sending message:', error);
          this.chatMessages.push({ messageText: 'Error sending message.....', isUser: false });
        }
      );

      console.log(value);
      // clear the chat input
      this.chatInput = "";
    }
  }
}
