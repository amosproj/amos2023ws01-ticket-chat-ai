import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
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
  title: string = "Talktix";
  chatInput: string = "";
  chatMessages: ChatMessages[] = [];

  constructor(private ticketService: TicketService) {}

  handleSend(value: string) {
    if (value) {
      this.chatMessages.push({ messageText: value, isUser: true });
  
      this.ticketService.send(value).subscribe(
        (response: any) => {
          const messageText = response.text; // Use "text" as per the backend API
          this.chatMessages.push({ messageText, isUser: false });
          console.log(response);
        },
        (error) => {
          console.error('Error sending message:', error);
          this.chatMessages.push({ messageText: 'Error sending message.....', isUser: false });
        }
      );
  
      console.log(value);
      this.chatInput = "";
    }
  }  
}
