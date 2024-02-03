from transformers import pipeline
from app.util.logger import logger
from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio
from sklearn.preprocessing import LabelEncoder


class AITicketService:
    def __init__(self):
        self.label_encoder = LabelEncoder()

        # Pipes
        self.title_generator_pipe = pipeline(
            "text2text-generation", model="czearing/article-title-generator"
        )
        self.affected_person_generator_pipe = pipeline(
            "token-classification", model="dslim/bert-base-NER"
        )
        self.keywords_generator_pipe = pipeline(
            "token-classification", model="ml6team/keyphrase-extraction-kbir-inspec"
        )
        self.request_type_generator_pipe = pipeline(
            "text-classification", model="TalkTix/roberta-base-request-type"
        )

        self.category_generator_pipe = pipeline(
            "text-classification",
            model="TalkTix/roberta-base-category-type-generator-53k",
        )

        self.service_generator_pipe = pipeline(
            "text-classification",
            model="TalkTix/roberta-base-service-type-generator-28k",
        )

        self.customer_priority_generator_pipe = pipeline(
            "text-classification",
            model="TalkTix/roberta-base-customer-priority-type-generator-28k",
        )

        self.priority_generator_pipe = pipeline(
            "text-classification",
            model="TalkTix/roberta-base-priority-type-generator-28k",
        )

        # Possible Field values
        self.request_type_values = ["Incident", "Service Request"]
        self.request_type_values.sort()

        self.service_values = [
            "SAP ERP",
            "Atlassian",
            "Adobe",
            "Salesforce",
            "Reporting",
            "Microsoft Power Platform",
            "Microsoft SharePoint",
            "Snowflake",
            "Microsoft Office",
        ]
        self.service_values.sort()

        self.category_values = [
            "Technical Issues",
            "Billing & Payment",
            "Product Inquiries",
            "Account Management",
            "Policy Questions",
        ]
        self.category_values.sort()

        self.customer_priority_values = [
            "Disruption but can work",
            "Disruption cannot work",
            "Disruption several cannot work",
            "Disruption department cannot work",
        ]
        self.customer_priority_values.sort()

        self.priority_values = ["Low", "Medium", "High", "Very High"]
        self.priority_values.sort()

    def create_ticket(self, input_text) -> dict:
        # generate prediction for each field
        title = self.generate_title(input_text)
        keywords = self.generate_keywords(input_text)
        affected_person = self.generate_affected_person(input_text)
        request_type = self.generate_prediction(
            input_text,
            self.request_type_generator_pipe,
            "requestType",
            self.request_type_values,
        )
        category = self.generate_prediction(
            input_text, self.category_generator_pipe, "category", self.category_values
        )
        service = self.generate_prediction(
            input_text, self.service_generator_pipe, "service", self.service_values
        )

        customer_priority = self.generate_prediction(
            input_text,
            self.customer_priority_generator_pipe,
            "customerPriority",
            self.customer_priority_values,
        )

        priority = self.generate_prediction(
            input_text, self.priority_generator_pipe, "priority", self.priority_values
        )

        # Create Ticket
        ticket_dict = {
            "title": title,
            "service": service,
            "category": category,
            "keywords": keywords,
            "customerPriority": customer_priority,
            "affectedPerson": affected_person,
            "description": input_text,
            "priority": priority,
            "requestType": request_type,
            "attachments": [],
        }

        return ticket_dict

    def generate_title(self, input_text) -> str:
        generated_title = self.title_generator_pipe(input_text)[0]["generated_text"]
        return generated_title

    def generate_affected_person(self, input_text) -> str:
        generated_output = self.affected_person_generator_pipe(input_text)

        if len(generated_output) > 0:
            persons = [
                entity["word"]
                for entity in generated_output
                if "PER" in entity["entity"]
            ]
            generated_affected_person = " ".join(persons)

            logger.info(
                "[AI] Prediction successfully generated. {}: {}".format(
                    "affectedPerson", generated_affected_person
                )
            )
            return generated_affected_person
        else:
            logger.info(
                "[AI] Could not generate prediction for Affected Person. Generated output is empty"
            )
            return ""

    def generate_keywords(self, input_text) -> list:
        generated_output = self.keywords_generator_pipe(input_text)

        if len(generated_output) > 0:
            keywords = [
                entity["word"].replace("Ġ", "")
                for entity in generated_output
                if "KEY" in entity["entity"]
            ]

            logger.info(
                "[AI] Prediction successfully generated. {}: {}".format(
                    "keywords", keywords
                )
            )
            return keywords
        else:
            logger.info("[AI] Could not generate keywords. Generated output is empty.")
            return []

    def generate_prediction(self, input_text, pipe, field, field_values) -> str:
        generated_output = pipe(input_text)
        prediction = None

        if len(generated_output) > 0:
            prediction_score = generated_output[0]["score"]
            if prediction_score < 0.5:
                logger.info(
                    "[AI] Could not generate prediction for {}. Prediction score are to worse.".format(
                        field
                    )
                )
                return prediction
            else:
                prediction = self.map_label_to_class(
                    generated_output[0]["label"], field_values
                )
                logger.info(
                    "[AI] Prediction successfully generated. {}: {}".format(
                        field, prediction
                    )
                )
                return prediction
        else:
            logger.info(
                "[AI] Could not generate prediction for {}. Generated output is empty".format(
                    field
                )
            )
            return prediction

    def map_label_to_class(self, label, classes) -> str:
        index = int(label[-1])
        return classes[index]

    # def remove_email_signature(self, email_content) -> str:
    #     parsed_email = EmailReplyParser.parse_reply(email_content)
    #     print("Generated parsed_email:", parsed_email)
    #     return parsed_email
