import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { catchError } from "rxjs/operators";
import { Observable } from "rxjs";
import { environment } from "../../environments/environment";
import { LogService } from './logging.service';

@Injectable({
  providedIn: "root"
})
export class TicketService {
  private apiUrl = environment.apiUrl + 'api/v1/ticket/text';

  constructor(private http: HttpClient, private logger: LogService) { }

  send(message: string, email: string): Observable<any> {
    const data = { text: message, email: email };

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

  sendFiles(files: File[], ticket_id: string): Observable<any> {
    // Create a FormData object
    const formData = new FormData();

    // Append each file to the FormData object
    files.forEach(file => {
      formData.append('files', file, file.name);
    });

    // Define headers for multipart/form-data
    const headers = new HttpHeaders({
      'Accept': 'application/json',
      // 'Content-Type': 'multipart/form-data' is not needed, Angular sets it automatically with boundary
    });

    const url = environment.apiUrl + 'api/v1/ticket/' + ticket_id + '/attachments';

    // Send POST request with formData and handle error
    return this.http.put(url, formData, { headers }).pipe(
      catchError((error) => {
        this.logger.log('Error sending files:' + error);
        throw error;
      })
    );
  }
}
