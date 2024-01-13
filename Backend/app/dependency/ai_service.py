from app.model.ai_service.ai_ticket_service import AITicketService


def get_ai_ticket_service() -> AITicketService:
    return AITicketService()
