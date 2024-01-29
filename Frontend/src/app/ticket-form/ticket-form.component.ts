import {Component, Input, OnInit} from '@angular/core';
import {Form, FormControl, FormGroup, Validators} from "@angular/forms";
import {Ticket} from "../entities/ticket.dto";
import {tick} from "@angular/core/testing";
import {TicketService} from "../service/ticket.service";
import {WrappedTicket} from "../entities/wrappedTicket.dto";
import {Prio} from "../entities/prio.enum";
import {RequestType} from "../entities/request-type";
import {MatChipEditedEvent, MatChipInputEvent} from "@angular/material/chips";
import {COMMA, ENTER} from "@angular/cdk/keycodes";

@Component({
  selector: 'app-ticket-form',
  templateUrl: './ticket-form.component.html',
  styleUrls: ['./ticket-form.component.css']
})
export class TicketFormComponent implements OnInit {
  @Input() wrappedTicket: WrappedTicket | undefined;

  ticketFormGroup: FormGroup | undefined;

  serviceValues = ["Atlassian", "Adobe"]
  categoryValues = ["Technical Issues", "Billing & Payment"]

  ngOnInit(): void {
    const ticket = this.wrappedTicket!.ticket!;
    this.ticketFormGroup = new FormGroup({
      title: new FormControl(ticket.title),
      description: new FormControl(ticket.description),
      keywords: new FormControl(ticket.keywords),
      service: new FormControl(ticket.service, [Validators.required]),
      category: new FormControl(ticket.category),
      requestType: new FormControl(ticket.requestType),
      priority: new FormControl(ticket.priority),
    });
  }

  submitTicket() {
    const ticket = this.wrappedTicket!.ticket!;

    ticket.category = this.ticketFormGroup!.value.category!;
    ticket.title = this.ticketFormGroup!.value.title!;
    ticket.description = this.ticketFormGroup!.value.description!;
    ticket.keywords = this.ticketFormGroup!.value.keywords!;
    ticket.service = this.ticketFormGroup!.value.service!;
    ticket.requestType = this.ticketFormGroup!.value.requestType!;
    ticket.priority = this.ticketFormGroup!.value.priority!;

    // this.ticketService.updateTicket(this.wrappedTicket, ticket.id);
  }

  protected readonly Prio = Prio;
  protected readonly RequestType = RequestType;

  removeKeyword(keyword: string) {
    this.ticketFormGroup!.value!.keywords = this.ticketFormGroup!.value!.keywords.filter((kw: string) => kw !== keyword);
  }

  editKeyword(keyword: string, event: MatChipEditedEvent) {
    const value = event.value.trim();
    this.ticketFormGroup!.value!.keywords = this.ticketFormGroup!.value!.keywords.filter((kw: string) => kw !== keyword);
    this.ticketFormGroup!.value!.keywords.push(value);
  }

  addKeyword(event: MatChipInputEvent) {
    const value = (event.value || '').trim();
    if (value) {
      this.ticketFormGroup!.value!.keywords.push(value);
    }
    event.chipInput!.clear();
  }

  protected readonly COMMA = COMMA;
  protected readonly ENTER = ENTER;
}
