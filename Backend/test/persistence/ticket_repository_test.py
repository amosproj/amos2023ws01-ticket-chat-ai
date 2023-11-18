from app.dto.enum.prio import Prio
from app.dto.enum.customer_prio import CustomerPrio
from app.dto.ticket import Ticket
from app.persistence.database_routine import start_server, stop_server
from app.persistence.ticket_repository import TicketRepository
import pytest

ticket_ds = TicketRepository()
ticket = Ticket(
    title="Test Ticket",
    location="Test the test ticket",
    category="",
    keywords=[],
    customerPriority=CustomerPrio.can_work,
    affectedPerson="",
    description="",
    priority=Prio.low,
)


@pytest.mark.skip(reason="Database Mock is missing")
def test_crud():
    # start db server
    system_status = start_server()
    assert system_status == 0

    # determine number of tickets in collection
    num_tickets = len(ticket_ds.read_tickets())
    assert num_tickets is not None

    # create ticket
    ticket_id = ticket_ds.create_ticket(ticket=ticket).inserted_id
    assert ticket_id is not None

    # read created ticket
    tickets = ticket_ds.read_tickets(ticket_id=ticket_id)
    assert len(tickets) == 1 and tickets[0]["_id"] == ticket_id

    # update ticket
    updated_ticket: Ticket = ticket.copy()
    updated_ticket.priority = Prio.medium
    update_result = ticket_ds.update_ticket(ticket_id=ticket_id, ticket=updated_ticket)
    assert update_result.modified_count == 1

    # read updated ticket
    tickets = ticket_ds.read_tickets(ticket_id=ticket_id)
    assert len(tickets) == 1 and tickets[0]["priority"] == Prio.medium

    # delete ticket
    delete_result = ticket_ds.delete_ticket(ticket_id=ticket_id)
    assert delete_result.deleted_count == 1

    # determine number of tickets in collection again
    new_num_tickets = len(ticket_ds.read_tickets())
    assert new_num_tickets == num_tickets

    # stop db server
    system_status = stop_server()
    assert system_status == 0
