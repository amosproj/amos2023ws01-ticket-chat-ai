from app.dto.prio_enum import PrioEnum
from app.dto.ticket import Ticket
from app.persistence.ticket_ds import TicketDS

ticket_ds = TicketDS()
ticket = Ticket(
    subject="Test Ticket",
    description="Test the test ticket",
    impact=PrioEnum.low,
    priority=PrioEnum.low,
    request_type="Problem"
)


def test_crud():
    # initially read empty collection
    tickets = ticket_ds.read_all_tickets()
    assert len(tickets) == 0
    # create ticket
    create_one_result = ticket_ds.create_ticket(ticket=ticket)
    assert create_one_result.inserted_id
    # read created ticket
    tickets = ticket_ds.read_all_tickets()
    assert len(tickets) == 1
    # update ticket
    updated_ticket: Ticket = ticket.copy()
    updated_ticket.priority = PrioEnum.medium
    update_result = ticket_ds.update_ticket(ticket_id=create_one_result.inserted_id, ticket=updated_ticket)
    assert update_result.modified_count == 1
    # read updated ticket
    tickets = ticket_ds.read_all_tickets()
    assert len(tickets) == 1 and tickets[0]["priority"] == PrioEnum.medium
    # delete ticket
    delete_result = ticket_ds.delete_ticket(ticket_id=create_one_result.inserted_id)
    assert delete_result.deleted_count == 1
    # finally read empty collection
    tickets = ticket_ds.read_all_tickets()
    assert len(tickets) == 0
