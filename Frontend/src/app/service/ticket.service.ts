import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { catchError } from "rxjs/operators";
import { Observable } from "rxjs";

@Injectable({
  providedIn: "root"
})
export class TicketService {
  private apiUrl = 'http://127.0.0.1:8000/api/v1/text';

  constructor(private http: HttpClient) {}

  send(message: string): Observable<any> {
    const data = { text: message };

    const headers = new HttpHeaders({
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    });

    return this.http.post(this.apiUrl, data, { headers }).pipe(
      catchError((error) => {
        console.error('Error sending message:', error);
        throw error;
      })
    );
  }
}
