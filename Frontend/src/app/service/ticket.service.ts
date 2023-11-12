import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http"

@Injectable({providedIn: "root"})
export class TicketService{
    constructor(private http: HttpClient){
    }
    send(message: string) {
        const url = 'http://localhost:8000/api/v1/text'; //answer with input
        
        const data= { messageText: message, isUser:true };

        return this.http.post(url, data);
    }
}
