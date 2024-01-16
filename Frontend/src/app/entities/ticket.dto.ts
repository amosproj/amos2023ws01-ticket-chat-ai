import {CustomerPrio} from "./customerPrio.enum";
import {Prio} from "./prio.enum";

export class Ticket{
    id: string = ""
    title: string = ""
    service: string = ""
    category: string = ""
    keywords = []
    customerPriority: CustomerPrio = CustomerPrio.can_work
    affectedPerson: string = ""
    description: string = ""
    priority: Prio = Prio.medium
    requestType: string = ""

  constructor(obj: any) {
    this.id = obj.id;
    this.title = obj.title;
    this.service = obj.service;
    this.category = obj.category;
    this.keywords = obj.keywords;
    this.customerPriority = obj.customerPriority;
    this.affectedPerson = obj.affectedPerson;
    this.description = obj.description;
    this.priority = obj.priority;
    this.requestType = obj.requestType;
  }

}
