import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http"

@Injectable({providedIn: "root"})
export class TicketService{
    constructor(private http: HttpClient){

    }

}
