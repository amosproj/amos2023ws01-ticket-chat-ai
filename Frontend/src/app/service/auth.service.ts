import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {tap, catchError} from 'rxjs/operators';
import {LogService} from './logging.service';
import {environment} from "../../environments/environment";
import {of} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl + 'api/v1/token';
  private apiUrl1 = environment.apiUrl + 'api/v1/verify-token';
  private apiUrl2 = environment.apiUrl + 'api/v1/signup';

  constructor(private http: HttpClient, private logger: LogService) {}

  login(email: string, password: string): Observable<any> {
    const loginData = new FormData();
    loginData.append('username', email);
    loginData.append('password', password);

    return this.http.post<{ access_token: string }>(this.apiUrl, loginData)
      .pipe(
        tap((response: { access_token: string }) => {
          // Save accessToken
          localStorage.setItem('access_token', response.access_token);
          this.logger.log('Login successful:'+ response);
          this.checkLoginStatus();
        }),
        catchError((error: any) => {
          let errorMessage = 'An error has occurred. Please try again later.';
          if (error.status === 400) {
            errorMessage = 'Login data not correct.';
          }
          this.logger.error('Login failed:'+ error);
          return of({ error: true, message: errorMessage });
        })
      );
  }

  signup(firstname: string, lastname: string, email: string, password: string, officeLocation: string): Observable<any> {
    return this.http.post<any>(this.apiUrl2, { firstname, lastname, email, password, officeLocation })
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: any) {
    let errorMessage = 'An unknown error occurred during signup.';
    if (error.error instanceof ErrorEvent) {
      // Client and Server Error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Backend Error report
      switch (error.status) {
        case 405:
          errorMessage = "Email is already in use.";
          break;
        // maybe mor cases
        default:
          if (error.error.detail) {
            errorMessage = `Error Code: ${error.status}\nMessage: ${error.error.detail}`;
          }
          break;
      }
    }
    return throwError(errorMessage);
  }


  checkLoginStatus(): void {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.logger.log('Token successful: ' + token);
    } else {
      this.logger.log('No token found, user is not logged in.');
    }
  }
  checkTokenValidity(): void {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      
      this.http.get<{ email: string }>(this.apiUrl1, {
        headers: { Authorization: `Bearer ${accessToken}` }
      }).subscribe({
        next: (response) => {
          this.logger.log('Token is valid. Logged in as: ' + response.email);
        },
        error: (error) => {
          localStorage.removeItem('access_token');
          this.logger.log('Token is invalid or expired. Logged out.');
        }
      });
    } else {
      this.logger.log('No token found, user is not logged in.');
    }
  }
}
