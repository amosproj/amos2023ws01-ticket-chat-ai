import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import {LogService} from './logging.service';
import {environment} from "../../environments/environment";
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl + 'api/v1/token';

  constructor(private http: HttpClient, private logger: LogService) {}

  login(email: string, password: string): Observable<any> {
    const loginData = new FormData();
    loginData.append('username', email);
    loginData.append('password', password);

    return this.http.post<{ access_token: string }>(this.apiUrl, loginData)
      .pipe(
        tap((response: { access_token: string }) => {
          // Speichern des Zugriffstokens
          localStorage.setItem('access_token', response.access_token);
          this.logger.log('Login successful:'+ response);
          this.checkLoginStatus();
        }),
        catchError((error: any) => {
          // Fehlerbehandlung
          let errorMessage = 'An error has occurred. Please try again later.';
          if (error.status === 400) {
            errorMessage = 'Login data not correct.';
          }
          this.logger.error('Login failed:'+ error);
          return of({ error: true, message: errorMessage });
        })
      );
  }

  checkLoginStatus(): void {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.logger.log('Token successful: ' + token); // Token-Informationen loggen
    } else {
      this.logger.log('No token found, user is not logged in.');
    }
  }
}
