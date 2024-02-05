import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {WrappedTicket} from "../entities/wrappedTicket.dto";
import {Prio} from "../entities/prio.enum";
import {RequestType} from "../entities/request-type";
import {MatChipEditedEvent, MatChipInputEvent} from "@angular/material/chips";
import {COMMA, ENTER} from "@angular/cdk/keycodes";
import {DbService} from "../service/db.service";
import {TicketService} from "../service/ticket.service";
import {State} from "../entities/state.enum";

@Component({
  selector: 'app-ticket-form',
  templateUrl: './ticket-form.component.html',
  styleUrls: ['./ticket-form.component.css']
})
export class TicketFormComponent implements OnInit {
  @Input() wrappedTicket: WrappedTicket | undefined;
  @Output() msgAfterButtonClick = new EventEmitter<string>();

  ticketFormGroup: FormGroup | undefined;

  serviceValues: string[] = [];
  categoryValues: string[] = [];
  isFormDisabled: boolean = false;

  constructor(private readonly dbService: DbService, private readonly ticketService: TicketService) {
  }

  ngOnInit(): void {
    const ticket = this.wrappedTicket!.ticket!;
    this.dbService.getServices().subscribe(services => {
      this.serviceValues = services;
      this.serviceValues.push(ticket.service);
    });
    this.dbService.getCategories().subscribe(categories => this.categoryValues = categories);
    this.ticketFormGroup = new FormGroup({
      title: new FormControl(ticket.title, [Validators.required]),
      description: new FormControl(ticket.description, [Validators.required]),
      keywords: new FormControl(ticket.keywords),
      service: new FormControl(ticket.service, [Validators.required]),
      category: new FormControl(ticket.category, [Validators.required]),
      requestType: new FormControl(ticket.requestType, [Validators.required]),
      priority: new FormControl(ticket.priority, [Validators.required]),
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
    ticket.state = State.accepted;

    this.ticketService.updateTicket(this.wrappedTicket!, ticket.id).subscribe();
    this.ticketFormGroup?.disable();
    this.isFormDisabled = true;
    this.msgAfterButtonClick.emit("Great, I've created your ticket! You will also receive a confirmation to the e-mail address you provided.");
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

  onCancelTicket() {
    this.ticketService.deleteTicket(this.wrappedTicket?.ticket?.id!).subscribe();
    this.ticketFormGroup?.disable();
    this.ticketFormGroup?.reset();
    this.isFormDisabled = true;
    this.msgAfterButtonClick.emit("All right, as you requested, the ticket has been cancelled.");
  }
}
