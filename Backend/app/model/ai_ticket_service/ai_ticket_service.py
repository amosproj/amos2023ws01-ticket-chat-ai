from transformers import pipeline
from app.util.logger import logger
from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio


class AITicketService:
    def __init__(self):
        self.title_generation_pipe = pipeline(
            "text2text-generation", model="czearing/article-title-generator"
        )
        self.affected_person_generation_pipe = pipeline(
            "token-classification", model="dslim/bert-base-NER"
        )
        self.keywords_generation_pipe = pipeline(
            "token-classification", model="ml6team/keyphrase-extraction-kbir-inspec"
        )

    def create_ticket(self, input_text) -> dict:
        title = self.generate_title(input_text)
        keywords = self.generate_keywords(input_text)
        affected_person = self.generate_affected_person(input_text)

        ticket_dict = {
            "title": title,
            "location": "",
            "category": "",
            "keywords": keywords,
            "customerPriority": CustomerPrio.can_work,
            "affectedPerson": affected_person,
            "description": input_text,
            "priority": Prio.low,
            "requestType": "",
            "attachments": [],
        }

        return ticket_dict

    def generate_title(self, input_text) -> str:
        generated_title = self.title_generation_pipe(input_text)[0]["generated_text"]
        return generated_title

    def generate_affected_person(self, input_text) -> str:
        generated_output = self.affected_person_generation_pipe(input_text)

        if len(generated_output) > 0:
            persons = [
                entity["word"]
                for entity in generated_output
                if "PER" in entity["entity"]
            ]
            generated_affected_person = " ".join(persons)

            return generated_affected_person
        else:
            logger.error("AI: Could not generate Affected Person")
            return ""

    def generate_keywords(self, input_text) -> list:
        generated_output = self.keywords_generation_pipe(input_text)

        if len(generated_output) > 0:
            keywords = [
                entity["word"]
                for entity in generated_output
                if "KEY" in entity["entity"]
            ]
            return keywords
        else:
            logger.error("AI: Could not generate keywords")
            return []

    # def remove_email_signature(self, email_content) -> str:
    #     parsed_email = EmailReplyParser.parse_reply(email_content)
    #     print("Generated parsed_email:", parsed_email)
    #     return parsed_email
