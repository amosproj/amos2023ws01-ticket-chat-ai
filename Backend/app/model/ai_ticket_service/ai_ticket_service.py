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
        self.request_type_generation_pipe = pipeline(
            "text-classification", model="TalkTix/roberta-base-request-type"
        )

    def create_ticket(self, input_text) -> dict:
        title = self.generate_title(input_text)
        keywords = self.generate_keywords(input_text)
        affected_person = self.generate_affected_person(input_text)
        request_type = self.generate_request_type(input_text)

        ticket_dict = {
            "title": title,
            "location": "",
            "category": "",
            "keywords": keywords,
            "customerPriority": CustomerPrio.can_work,
            "affectedPerson": affected_person,
            "description": input_text,
            "priority": Prio.low,
            "requestType": request_type,
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
            logger.info("AI: Could not generate keywords")
            return []

    def generate_request_type(self, input_text) -> str:
        generated_output = self.request_type_generation_pipe(input_text)
        request_type_values = ["Incident", "Service Request"]
        print(generated_output)

        if len(generated_output) > 0:
            prediction_score = max(generated_output['score'])
            if prediction_score < 0:
                logger.info("AI: Request type prediction is to worse")
                return ""
        else:
            logger.info("AI: Could not generate request type")
            return ""



    # def remove_email_signature(self, email_content) -> str:
    #     parsed_email = EmailReplyParser.parse_reply(email_content)
    #     print("Generated parsed_email:", parsed_email)
    #     return parsed_email
