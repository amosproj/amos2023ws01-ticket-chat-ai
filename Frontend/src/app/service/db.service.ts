import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable, throwError } from "rxjs";
import { catchError } from "rxjs/operators";
import { environment } from "../../environments/environment";
import { LogService } from './logging.service';

@Injectable({
  providedIn: "root"
})
export class DbService {
  private servicesApiUrl = environment.apiUrl + 'api/v1/services';
  private categoriesApiUrl = environment.apiUrl + 'api/v1/categories';

  constructor(private http: HttpClient, private logger: LogService) {
  }

  getServices(): Observable<string[]> {
    return this.http.get<string[]>(this.servicesApiUrl).pipe(
      catchError(error => {
        this.logger.log('Error fetching services: ' + error);
        return throwError(() => new Error('Error fetching services. Please try again later.'));
      })
    );
  }

  getCategories(): Observable<string[]> {
    return this.http.get<string[]>(this.categoriesApiUrl).pipe(
      catchError(error => {
        this.logger.log('Error fetching categories: ' + error);
        return throwError(() => new Error('Error fetching categories. Please try again later.'));
      })
    );
  }
}
