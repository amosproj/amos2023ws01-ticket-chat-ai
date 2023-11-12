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
    /**
     * Gets called when send button is pressed
     * @param {string} value - Text from the Input
     */
    if (value){   //we dont want to send empty messages to backend
      this.chatMessages.push({messageText: value, isUser: true});
      
      this.ticketService.send(value).subscribe((response: any) => {
        const messageText = response.messageText;

        this.chatMessages.push({ messageText, isUser: false }); // Assuming it's a response from the server
        console.log(response);
      },
      (error) => {
        console.error('Error sending message:', error);
      });
      console.log(value);
      this.chatInput = "";
    }  
  }
}
