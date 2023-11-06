import { Injectable } from "@angular/core";
import { HttpClient, HttpClientModule } from "@angular/common/http"

@Injectable({providedIn: "root"})
export class TicketService{
    constructor(private http: HttpClient){
    }
    send(message: string) {
        const url = 'https://reqres.in/api/posts'; //answer with input
        
        const data= { messageText: message, isUser:true };

        return this.http.post(url, data,);
    }
}
