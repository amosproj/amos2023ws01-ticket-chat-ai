import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { catchError } from "rxjs/operators";
import { Observable } from "rxjs";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: "root"
})
export class TicketService {
  private apiUrl = environment.apiUrl + 'api/v1/text';

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
