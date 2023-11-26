import { Injectable } from "@angular/core";

@Injectable({
    providedIn: "root"
  })
export class LogService {
    error(msg: any){
        console.error(new Date() + ": " + JSON.stringify(msg), 'color: #DC143C');
    }

    log(msg: any){
        console.log(new Date() + ": " + JSON.stringify(msg));
    }
}
