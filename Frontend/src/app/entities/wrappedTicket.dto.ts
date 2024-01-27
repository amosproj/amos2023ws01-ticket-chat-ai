import {CustomerPrio} from "./customerPrio.enum";
import {Prio} from "./prio.enum";
import {State} from "./state.enum";
import {Ticket} from "./ticket.dto";

export class WrappedTicket{
    email: string = "";
    ticket: Ticket | undefined;
}
