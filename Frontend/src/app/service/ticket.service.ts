import {Injectable} from "@angular/core";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {catchError} from "rxjs/operators";
import {Observable, throwError} from "rxjs";
import {environment} from "../../environments/environment";
import {LogService} from './logging.service';
import {Ticket} from "../entities/ticket.dto";
import {WrappedTicket} from "../entities/wrappedTicket.dto";

@Injectable({
  providedIn: "root"
})
export class TicketService {
  private apiUrl = environment.apiUrl + 'api/v1/ticket/text';

  constructor(private http: HttpClient, private logger: LogService) {
  }

  send(message: string, email: string): Observable<any> {
    if (!message) {
      return throwError('Please write a message or leave a voice message.');
    }

    const data = {text: message, email: email};

    // define headers
    const headers = new HttpHeaders({
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    });

    // send post request and handle error
    return this.http.post(this.apiUrl, data, {headers}).pipe(
      catchError((error) => {
        this.logger.log('Error sending message:' + error);
        return throwError('Unfortunately an error has occurred. Please try again or try again later, we apologize.');
      })
    );
  }

  updateTicket(wrappedTicket: WrappedTicket, ticket_id: string): Observable<any> {
    const url = environment.apiUrl + 'api/v1/ticket/' + ticket_id + '/update';

    // define headers
    const headers = new HttpHeaders({
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    });

    return this.http.put(url, wrappedTicket, {headers}).pipe(
      catchError((error) => {
        this.logger.log('Error while updating ticket: ' + error);
        return throwError('An Error occurred. Please try again later.');
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
    return this.http.put(url, formData, {headers}).pipe(
      catchError((error) => {
        this.logger.log('Error sending files:' + error);
        return throwError('Unfortunately an error has occurred. Please try again or try again later, we apologize.');
      })
    );
  }
}
