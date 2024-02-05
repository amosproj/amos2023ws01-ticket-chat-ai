import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, throwError, of} from 'rxjs';
import {tap, catchError, map} from 'rxjs/operators';
import {LogService} from './logging.service';
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl + 'api/v1/token';
  private apiUrl1 = environment.apiUrl + 'api/v1/verify-token';
  private apiUrl2 = environment.apiUrl + 'api/v1/signup';
  private apiUrl3 = environment.apiUrl + 'api/v1/edit';
  private apiUrl4 = environment.apiUrl + 'api/v1/getuserinfo';

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

  signup(first_name: string, family_name: string, email: string, password: string, location: string): Observable<any> {
    return this.http.post<any>(this.apiUrl2, { first_name, family_name, email, password, location })
      .pipe(
        catchError(this.handleError)
      );
  }

  edit(old_email: string, old_password: string, first_name: string, family_name: string, email: string, password: string, location: string): Observable<any> {
    return this.http.post<any>(this.apiUrl3, { old_email, old_password, first_name, family_name, email, password, location })
      .pipe(
        catchError(this.handleError)
      );
  }

  getuserinfo(email: string): Observable<any> {
    return this.http.post<any>(this.apiUrl4, { email })
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
  checkTokenValidity(): Observable<boolean> {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      return this.http.get<{ email: string }>(this.apiUrl1, {
        headers: { Authorization: `Bearer ${accessToken}` }
      }).pipe(
        map(response => {
          this.logger.log('Token is valid. Logged in as: ' + response.email);
          return true;
        }),
        catchError((error) => {
          localStorage.removeItem('access_token');
          this.logger.log('Token is invalid or expired. Logged out.');
          return of(false);
        })
      );
    } else {
      this.logger.log('No token found, user is not logged in.');
      return of(false);
    }
  }
}
