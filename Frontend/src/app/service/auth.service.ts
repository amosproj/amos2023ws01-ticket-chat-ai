import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { delay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() { }

  login(email: string, password: string): Observable<{success: boolean, message?: string}> {
    // here Http-Request to Backend
    // simulation of network delay 1s
    return of({success: password === "dummy"}).pipe(delay(1000));
  }
}
