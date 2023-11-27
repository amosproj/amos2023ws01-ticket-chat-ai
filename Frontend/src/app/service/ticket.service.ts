import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { catchError } from "rxjs/operators";
import { Observable } from "rxjs";
import {environment} from "../../environments/environment";
import { LogService } from './logging.service';

@Injectable({
  providedIn: "root"
})
export class TicketService {
  private apiUrl = environment.apiUrl + 'api/v1/text';

  constructor(private http: HttpClient, private logger: LogService) {}

  send(message: string): Observable<any> {
    const data = { text: message };

    // define headers
    const headers = new HttpHeaders({
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    });

    // send post request and handle error
    return this.http.post(this.apiUrl, data, { headers }).pipe(
      catchError((error) => {
        this.logger.log('Error sending message:' + error);
        throw error;
      })
    );
  }
}
