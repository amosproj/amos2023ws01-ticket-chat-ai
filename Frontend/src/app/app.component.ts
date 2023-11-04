import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

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

  handleSend(value: string) {
    /**
     * Gets called when send button is pressed
     * @param {string} value - Text from the Input
     */
    if (value){   //we dont want to send empty messages to backend
      this.chatMessages.push({messageText: value, isUser: true});
      console.log(value);
      this.chatInput = "";
    }  
  }
}
